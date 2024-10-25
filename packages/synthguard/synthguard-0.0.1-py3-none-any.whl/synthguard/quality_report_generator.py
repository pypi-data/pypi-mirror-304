import matplotlib.pyplot as plt
from sdv.evaluation.single_table import evaluate_quality
from sdmetrics.visualization import get_column_plot

class DataQualityEvaluator:
    def __init__(self, real_data, synthetic_data, metadata, method='sdv'):
        """
        Initializes the DataQualityEvaluator with the given parameters.

        Args:
            real_data (pd.DataFrame): The real data as a pandas DataFrame.
            synthetic_data (pd.DataFrame): The synthetic data as a pandas DataFrame.
            metadata (Metadata): Metadata object describing the dataset.
            method (str): The method used for evaluation, default is 'sdv'.
        """
        self.synthetic_data = synthetic_data
        self.real_data = real_data
        self.metadata = metadata
        self.method = method
        self.quality_report = None  # Initialize quality_report as None

    def evaluate_quality(self):
        """Evaluates the quality of synthetic data."""
        if self.method == 'sdv':
            self.quality_report = self.evaluate_quality_sdv()
            return self.quality_report
        else:
            raise ValueError(f"Unknown evaluation method: {self.method}")

    def evaluate_quality_sdv(self):
        """Evaluates quality using the SDV method."""
        quality_report = evaluate_quality(
            real_data=self.real_data,
            synthetic_data=self.synthetic_data,
            metadata=self.metadata
        )
        print("Quality report generated.")
        return quality_report

    def get_score(self):
        """Retrieves the overall score of the quality report."""
        return self.quality_report.get_score()

    def get_properties(self):
        """Retrieves the properties evaluated in the quality report."""
        return self.quality_report.get_properties()

    def get_details(self, property_name):
        """Gets detailed information about a specific property in the quality report.

        Args:
            property_name (str): The name of the property to get details for.

        Returns:
            pd.DataFrame: Detailed scores for the specified property.
        """
        return self.quality_report.get_details(property_name)

    def visualize_quality_report(self):
        """Visualizes the quality report scores as a pie chart."""
        try:
            scores = self.get_properties()
            labels = scores['Property'].tolist()
            sizes = scores['Score'].tolist()
            colors = ['#ff9999', '#66b3ff', '#99ff99']  # Different colors for each slice

            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('Quality Report Visualization')
            plt.show()
        except Exception as e:
            print(f"An error occurred while visualizing the quality report: {e}")

    def visualize_property(self, property_name):
        """Visualizes the details of a specific property in the quality report.

        Args:
            property_name (str): The name of the property to visualize.
        """
        fig = self.quality_report.get_visualization(property_name=property_name)
        fig.show()

    def compare_columns(self):
        """Compares synthetic and real columns and visualizes the results."""
        for column in self.real_data.columns:
            if column in self.synthetic_data.columns:
                print(f"Comparing column: {column}")
                try:
                    # Pass the entire DataFrame for each column comparison
                    fig = get_column_plot(
                        real_data=self.real_data,  # Pass entire DataFrame
                        synthetic_data=self.synthetic_data,  # Pass entire DataFrame
                        column_name=column,  # Column name to plot
                        plot_type='bar'  # Determine plot type automatically
                    )
                    fig.show()
                except Exception as e:
                    print(f"An error occurred while visualizing column {column}: {e}")

    def univariate_fidelity(self):
        """Placeholder for univariate fidelity evaluation."""
        print("Evaluating univariate fidelity...")
        return "univariate_fidelity_score"

    def bivariate_fidelity(self):
        """Placeholder for bivariate fidelity evaluation."""
        print("Evaluating bivariate fidelity...")
        return "bivariate_fidelity_score"

    def utility_analysis(self):
        """Placeholder for utility analysis."""
        print("Performing data utility analysis...")
        return "utility_analysis_score"
