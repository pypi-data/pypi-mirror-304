import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import numpy as np
from attrs import define, field

from gerg_plotting.plotting_classes.Plotter import Plotter
from gerg_plotting.utils import get_sigma_theta, get_density
from gerg_plotting.data_classes.NonSpatialInstruments import Variable

@define
class ScatterPlot(Plotter):
    """
    ScatterPlot class for creating various scatter plots from a SpatialInstrument's data.

    Inherits from the Plotter class to leverage figure, axis, and colorbar management functionalities.
    This class specifically deals with scatter plots that visualize relationships between different variables
    (e.g., temperature vs salinity, time vs depth) in the provided instrument data.
    
    Attributes:
        markersize (int | float): The size of the scatter plot markers.
    """
    
    markersize: int | float = field(default=10)

    def format_axes(self):
        """
        Method to format the axes.

        This method can be extended to apply more specific formatting to the axes, like setting labels, 
        tick formatting, gridlines, etc.
        """
        self.ax.yaxis  # Placeholder for additional formatting logic
        
    
    def depth_time_series(self, var: str, fig=None, ax=None, contours: bool = False) -> None:
        """
        Create a scatter plot of depth vs time, with color representing the given variable `var`.
        
        Args:
            var (str): The variable to plot as color.
            fig (matplotlib.figure.Figure, optional): The figure to use for the plot. If None, a new figure is created.
            ax (matplotlib.axes.Axes, optional): The axes to use for the plot. If None, new axes are created.
            contours (bool, optional): Whether to include contour lines.
        
        This method initializes a figure and axes, creates a scatter plot of depth vs. time, and adds a colorbar.
        """
        self.init_figure(fig, ax)  # Initialize figure and axes
        sc = self.ax.scatter(
            self.instrument.time.data,
            self.instrument.depth.data,
            c=self.instrument[var].data,
            cmap=self.instrument[var].cmap,
            s=self.markersize
        )  # Create scatter plot with color mapped to `var`
        
        self.ax.invert_yaxis()  # Invert the y-axis to have depth increasing downward
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)

        self.ax.xaxis.set_major_locator(locator)  # Set date locator for x-axis
        self.ax.xaxis.set_major_formatter(formatter)  # Set date formatter for x-axis
        matplotlib.pyplot.xticks(rotation=60, fontsize='small')  # Rotate x-axis labels for readability
        self.add_colorbar(sc, var=var)  # Add colorbar to the plot

    def check_ts(self, color_var: str = None) -> None:
        """
        Check if the instrument contains the required variables for a temperature-salinity (T-S) diagram.
        
        Args:
            color_var (str, optional): Additional variable to check for existence.
        
        Raises:
            ValueError: If the instrument lacks required variables like salinity or temperature, or the given color_var.
        """
        if not self.instrument._has_var('salinity'):
            raise ValueError('Instrument has no salinity attribute')
        if not self.instrument._has_var('temperature'):
            raise ValueError('Instrument has no temperature attribute')
        if color_var is not None and not self.instrument._has_var(color_var):
            raise ValueError(f'Instrument has no {color_var} attribute')

    def format_ts(self, fig, ax, contours: bool = True) -> None:
        """
        Prepare a temperature-salinity (T-S) diagram with optional contour lines.
        
        Args:
            fig (matplotlib.figure.Figure): The figure to use.
            ax (matplotlib.axes.Axes): The axes to use.
            contours (bool, optional): Whether to include density contour lines (default is True).
        
        This method initializes the figure and axes, adds contour lines for sigma-theta if requested, 
        and applies axis labels and formatting for a T-S diagram.
        """
        self.check_ts()  # Check if instrument contains required variables
        self.init_figure(fig, ax)  # Initialize figure and axes

        if contours:
            # Calculate sigma-theta contours
            Sg, Tg, sigma_theta = get_sigma_theta(
                salinity=self.instrument['salinity'].data,
                temperature=self.instrument['temperature'].data
            )
            cs = self.ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1, linestyles='dashed')
            matplotlib.pyplot.clabel(cs, fontsize=10, inline=True, fmt='%.1f')  # Add contour labels

        self.ax.set_xlabel('Salinity')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.set_title('T-S Diagram', fontsize=14, fontweight='bold')  # Add title
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # Set x-axis tick formatting
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

    def TS(self, fig=None, ax=None, contours: bool = True) -> None:
        """
        Create a temperature vs salinity scatter plot, with optional contours.
        
        Args:
            fig (matplotlib.figure.Figure, optional): The figure to use.
            ax (matplotlib.axes.Axes, optional): The axes to use.
            contours (bool, optional): Whether to include sigma-theta contour lines (default is True).
        
        This method plots salinity vs. temperature, with optional sigma-theta contour lines.
        """
        self.format_ts(fig, ax, contours)  # Prepare T-S diagram layout
        self.ax.scatter(
            self.instrument['salinity'].data,
            self.instrument['temperature'].data,
            s=self.markersize,
            marker='.'
        )  # Scatter plot of salinity vs temperature

    def get_density_color_data(self, color_var: str) -> np.ndarray:
        """
        Retrieve the color data for a variable, or calculate density if requested.
        
        Args:
            color_var (str): The variable for which to retrieve color data.
        
        Returns:
            np.ndarray: The color data for the scatter plot.
        
        If the color variable is 'density' and the instrument does not already have density data, this method 
        calculates it from salinity and temperature.
        """
        if color_var == 'density':
            if not isinstance(self.instrument['density'], Variable):  # If density is not already provided
                color_data = get_density(
                    self.instrument['salinity'].data,
                    self.instrument['temperature'].data
                )  # Calculate density from salinity and temperature
            else:
                color_data = self.instrument[color_var].data
        else:
            color_data = self.instrument[color_var].data  # Retrieve color data for the specified variable

        return color_data

    def TS_with_color_var(self, color_var: str, fig=None, ax=None, contours: bool = True) -> None:
        """
        Create a temperature vs salinity scatter plot, with color representing another variable.
        
        Args:
            color_var (str): The variable to map to color in the scatter plot.
            fig (matplotlib.figure.Figure, optional): The figure to use.
            ax (matplotlib.axes.Axes, optional): The axes to use.
            contours (bool, optional): Whether to include sigma-theta contour lines (default is True).
        
        This method plots salinity vs. temperature, with the color of each point determined by the specified `color_var`.
        """
        self.format_ts(fig, ax, contours)  # Prepare T-S diagram layout
        cmap = self.get_cmap(color_var)  # Get colormap for the color variable
        color_data = self.get_density_color_data(color_var)  # Get color data (or calculate density if needed)

        sc = self.ax.scatter(
            self.instrument['salinity'].data,
            self.instrument['temperature'].data,
            c=color_data,
            s=self.markersize,
            marker='.',
            cmap=cmap
        )  # Scatter plot with color representing `color_var`
        
        self.add_colorbar(sc, color_var)  # Add a colorbar to the plot

    def var_var(self, x: str, y: str, color_var: str | None = None, fig=None, ax=None) -> None:
        """
        Create a scatter plot of two variables `x` and `y`, with optional coloring by a third variable.
        
        Args:
            x (str): The variable to plot on the x-axis.
            y (str): The variable to plot on the y-axis.
            color_var (str | None, optional): The variable to map to color (default is None).
            fig (matplotlib.figure.Figure, optional): The figure to use.
            ax (matplotlib.axes.Axes, optional): The axes to use.
        
        This method creates a scatter plot of the variables `x` and `y`, with optional coloring by `color_var`.
        """
        self.init_figure(fig, ax)  # Initialize figure and axes

        if color_var is not None:
            sc = self.ax.scatter(
                self.instrument[x].data,
                self.instrument[y].data,
                c=self.instrument[color_var].data,
                cmap=self.get_cmap(color_var)
            )  # Scatter plot with color representing `color_var`
            self.add_colorbar(sc, var=color_var)  # Add colorbar
            self.format_axes()  # Apply any additional axis formatting
        else:
            self.ax.scatter(self.instrument[x].data, self.instrument[y].data)  # Scatter plot without color variable

    def cross_section(self, longitude, latitude) -> None:
        """
        Method placeholder for plotting cross-sections.

        Args:
            longitude: Longitude data for the cross-section.
            latitude: Latitude data for the cross-section.
        
        Raises:
            NotImplementedError: Indicates that the method is not yet implemented.
        """
        raise NotImplementedError('Need to add method to plot cross sections')
