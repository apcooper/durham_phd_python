import matplotlib.pyplot as pl
import numpy as np
import matplotlib.gridspec as gridspec

def fancy_dotplot(xyz,project_axis=0):
    """
    """
    f = pl.figure(figsize=(3,3))

    iproj = [0,1,2]
    iproj.remove(project_axis)
    ix,iy = iproj
   
    nrow, ncol = 2,2
    gs         = gridspec.GridSpec(nrow,ncol,
                                   wspace=0.0,hspace=0.0,
                                   height_ratios=(0.2,1),
                                   width_ratios=(1,0.2))

    x, y = xyz[:,ix],xyz[:,iy]
    xmin = 0.90*x.min()
    xmax = 1.10*x.max()
    ymin = 0.90*y.min()
    ymax = 1.10*y.max()

    # Main plot
    irow,icol = 1,0
    main_ax = pl.subplot(gs[irow,icol])
    main_ax.scatter(x,y,s=3,edgecolor='None',c='w')
    pl.hist2d(x,y,
              bins=(np.linspace(xmin,xmax,20),np.linspace(ymin,ymax,20)),
              cmap='viridis',alpha=0.8)
    pl.xlim(xmin,xmax)
    pl.ylim(ymin,ymax)
    
    irow,icol = 0,0
    ax = pl.subplot(gs[irow,icol])
    ax.hist(x,bins=np.linspace(xmin,xmax,20),color='k')
    pl.setp(ax.get_xticklabels(),visible=False)
    pl.setp(ax.get_yticklabels(),visible=False)
    pl.xlim(xmin,xmax)
    
    irow,icol = 1,1
    ax = pl.subplot(gs[irow,icol])
    ax.hist(y,bins=np.linspace(ymin,ymax,20),orientation='horizontal',color='k')
    pl.setp(ax.get_xticklabels(),visible=False)
    pl.setp(ax.get_yticklabels(),visible=False)
    pl.ylim(ymin,ymax)
    
    pl.sca(main_ax)
    
    # Trim the tick labels from the end of each axis
    pl.setp(main_ax.get_xticklabels()[0],visible=False)
    pl.setp(main_ax.get_xticklabels()[-1],visible=False)
    pl.setp(main_ax.get_yticklabels()[0],visible=False)
    pl.setp(main_ax.get_yticklabels()[-1],visible=False)
    
    pl.xlabel('Axis %d'%(ix))
    pl.ylabel('Axis %d'%(iy))
    
    pl.draw()
    pl.savefig('w2challenge_dotplot_%d.png'%(project_axis),bbox_inches='tight',pad_inches=0.1)
    return

if __name__ == '__main__':
    # Run the plot
    np.random.seed(42)
    coordinates = np.random.normal(1,1,(1000,3))
    fancy_dotplot(coordinates,0)
    fancy_dotplot(coordinates,1)
    fancy_dotplot(coordinates,2)