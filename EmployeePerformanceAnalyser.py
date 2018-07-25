import matplotlib.pyplot as plt
import pandas as pd


class EmployeePerformanceAnalyser(object):
    def __init__(self, employee_data="EmployeeDataFull.msg"):
        self.data_file = employee_data
        self.data_frame = pd.read_msgpack(self.data_file)
        self.column = ["PRESSED CHAR", "PRESSED COUNT", "RELEASED CHAR", "RELEASED COUNT",
                       "MOUSE MOVE COUNT","MOUSE CLICKED COUNT", "MOUSE SCROLLED COUNT", "FINAL COUNT"]
        self.empty_data = [["N/A", 0, "N/A", 0, 0, 0, 0, 0]]
        self.empty_index = None
        Plot_Graph = self.data_frame[['FINAL COUNT']].plot(kind='line', title="Performance Monitor", legend=True, fontsize=12)
        Plot_Graph.set_xlabel("Minutes", fontsize=12)
        Plot_Graph.set_ylabel("Process Done", fontsize=12)
        plt.show()

    def data_synchronize(self, start_date, end_date):
        """
        For synchronize the missing data with empty string and sorting it accoridng to index.
        :rtype: object
        """
        for date in range(start_date, end_date):
            for hour in range(0, 23):
                for minute in range(0, 59):
                    self.empty_index = "18/07/{0}_{1}:{2}".format(str(date).zfill(2), str(hour).zfill(2),
                                                                  str(minute).zfill(2))
                    if not self.empty_index in self.data_frame.index:
                        self.data_frame = self.data_frame.append(
                            pd.DataFrame(data=self.empty_data, columns=self.column, index=[self.empty_index]))
        self.data_frame.sort_index(inplace=True)
        self.data_frame.to_msgpack(self.data_file)


if __name__ == '__main__':
    ROOT = EmployeePerformanceAnalyser()
