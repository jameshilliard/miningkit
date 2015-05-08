'''
Helper to work with line chart

Example:
chart = LineChart(5)
chart.lines() => [[0, 0, 0, 0, 0]]
chart.append([1])
chart.lines() => [[0, 0, 0, 0, 1]]
chart.append([5])
chart.lines() => [[0, 0, 0, 1, 5]]

Adding array with different lenght (for example now you want to work with 2 lines) will reset line chart
chart.append([10, 20])
chart.lines() => [[0, 0, 0, 0, 10], [0, 0, 0, 0, 20]]
chart.append([15, 5])
chart.lines() => [[0, 0, 0, 10, 15], [0, 0, 0, 20, 5]]
chart.append([1, 3, 5])
chart.lines() => [[0, 0, 0, 0, 1], [0, 0, 0, 0, 3], [0, 0, 0, 0, 5]]

Reset chart by providing lines quantity
chart.reset(1)
chart.lines() => [[0, 0, 0, 0, 0]]
chart.reset(3)
chart.lines() => [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
'''
class LineChart:

    def __init__(self, line_length):
        pass

    def lines(self):
        pass

    def append(self, points):
        pass

    def reset(self, lines_quantity):
        pass
