import numpy as np
import matplotlib.pyplot as pl
import os
import sys

def plot_challenge(input_file):
    """
    Reads data from input file and 
    """    
    # We want random but reproducible results, so 
    # set the seed explictly:
    np.random.seed(42)

    # The number of CCD pixels in each dimension
    nx, ny = 100, 100
    
    # Read the input data from the file provided. 
    # Use usecols= to skip the first column because 
    # it's got strings in it.
    x,y,flux,fwhm = np.loadtxt(input_file,usecols=[1,2,3,4],
                               unpack=True,dtype=np.float32)

    # If we also wanted the strings in the first column,
    # we could get them separately.
    # names         = np.loadtxt(input_file,usecols=[0],dtype='str')
    
    # Store the number of sources.
    # This is just for readability later on.
    n_sources = len(x)
    
    # Set up the CCD pixels as a numpy array
    ccd_pixels = np.zeros((nx,ny),dtype=np.float64)
    
    # My strategy is to generate a Gaussian distribution
    # of counts for each source in its own 100x100 array, 
    # each of which gets added to the 'master' ccd_pixels
    # array defined above to build up the final image.
    
    # Loop over the sources.
    for i in xrange(0,n_sources):
        n_counts = int(flux[i]) # Number of counts for this source.
        dim      = (n_counts,2) # Dimensions of the array of random photon coordinates
        
        # Randomly generate N photons for this source. 
        # We can pass 2D positions to the numpy function 
        # random.normal, which draws random numbers from
        # a Gaussian distribution. We can ask for the size
        # of the random array to be 2d as well.
        photons   = np.random.normal(loc=(x[i],y[i]),scale=fwhm[i],size=dim)

        # The above is the same as:
        # photons_x = np.random.normal(loc=x[i],scale=fwhm[i],size=n_counts)
        # photons_y = np.random.normal(loc=y[i],scale=fwhm[i],size=n_counts)
        # photons   = np.array((photons_x,photons_y)).T
        # In this case, note the transpose operator .T, which gives an 
        # (N,2) array rather than a (2,N) array. The choice isn't important,
        # but being consistent about whichever convention you choose is!
        
        # Bin these points on on a grid with the same dimensions
        # as the CCD.
        bins                  = (np.arange(0,nx+1),np.arange(0,ny+1))
        binned_counts, bx, by = np.histogram2d(photons[:,0],
                                               photons[:,1],
                                               bins=bins)
        
        # Add this component to the CCD image.
        ccd_pixels         = ccd_pixels + binned_counts
    
    # Finally, add poisson noise (again taking advantage)
    background_mean_counts = 10
    ccd_pixels = ccd_pixels + np.random.poisson(background_mean_counts,
                                                size=(nx,ny))

    # Print the total flux and mean flux
    print('Total counts:  %e'%(np.sum(ccd_pixels)))
    print('Maximum count: %e'%(np.max(ccd_pixels)))

    # Make the plot
    f = pl.figure(figsize=(6,6))
    
    # Getting the orientation of the image to match the 
    # coordinates in the input file is tricky, because 
    # there are multiple conventions invovled for the 
    # 'origin' of the coordinate system. Specifically:
    #   - the X,Y convention in the input file
    #   - numpy's convention for the order of columns and rows
    #   - matplotlib's convention for imshow
    
    # This is easiest to understand with trial and error!
    # Note the transpose operator '.T' and origin='lower'
    pl.imshow(np.log10(ccd_pixels).T,
              vmin=-1,vmax=4,
              cmap='viridis',
              extent=(bx[0],bx[-1],by[0],by[-1]),
              interpolation='nearest',origin='lower')

    # You can check for yourself what the 'vmin', 'vmax', extent' 
    # and 'interpolation' keywords do.
    
    # We need a colourbar. We can resize the colourbar using
    # the 'shrink' argument.
    cbar = pl.colorbar(shrink=0.75)
    cbar.set_label(r'$\log_{10}\,\mathrm{counts}$',fontsize=12)
    
    # Finally we need to format the plot to get it to match the 
    # example example.
    
    # First we'll get the 'current axes' object so that we can
    # operate on it directly. The idea of a 'current figure'
    # and 'current axes' is important in matplotlib.
    ax = pl.gca()
    
    # Now apply some formatting to the axes object. 
    
    # First get rid of the tick labels at the 'ends' of 
    # each range.
    pl.setp(ax.get_xticklabels()[0], visible=False)
    pl.setp(ax.get_xticklabels()[-1],visible=False)
    pl.setp(ax.get_yticklabels()[0], visible=False)
    pl.setp(ax.get_yticklabels()[-1],visible=False)
    
    # Set the axis labels
    pl.xlabel('$\Delta X$',fontsize=12)
    pl.ylabel('$\Delta Y$',fontsize=12)

    # Finally, save the plot. Note the 'bbox_inches' and 
    # 'pad_inches' commands. These avoid problems with 
    # whitespace around the figure, which is important 
    # when making PDF or eps format plots to include in
    # a paper using LaTeX.
    output_path = './challenge.png'
    pl.savefig(output_path,bbox_inches='tight',pad_inches=0.1)
    print('Wrote output to: %s'%(os.path.abspath(output_path)))
    
    # This is just to show the figure in the notebook.
    pl.show()
    
    # Remember to close the figure.
    pl.close(f)
    return

# This block is executed if run from the command line
if __name__ == '__main__':
    input_file = sys.argv[1] # Get the first command line argument
    plot_challenge(input_file)