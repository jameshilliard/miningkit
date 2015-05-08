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
        self._line_length = line_length
        self._lines = []
        self.reset(1)

    def lines(self):
        return self._lines

    def append(self, points):
        if len(self._lines) != len(points):
            self.reset(len(points))

        for i, line in enumerate(self._lines):
            self._lines[i].pop(0)
            self._lines[i].append(points[i])

    def reset(self, number_of_lines):
        new_lines = []

        for i in xrange(1, number_of_lines + 1):
            new_lines.append([0 for x in xrange(1, self._line_length + 1)])

        self._lines = new_lines

if __name__ == '__main__':
    chart = LineChart(3)
    assert chart.lines() == [[0, 0, 0]]

    chart = LineChart(7)
    assert chart.lines() == [[0, 0, 0, 0, 0, 0, 0]]

    chart = LineChart(5)
    assert chart.lines() == [[0, 0, 0, 0, 0]]

    chart.reset(2)
    assert chart.lines() == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    chart.reset(3)
    assert chart.lines() == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    chart.append([1, 2, 3])
    assert chart.lines() == [[0, 0, 0, 0, 1], [0, 0, 0, 0, 2], [0, 0, 0, 0, 3]]

    chart.append([10, 20, 30])
    assert chart.lines() == [[0, 0, 0, 1, 10], [0, 0, 0, 2, 20], [0, 0, 0, 3, 30]]

    chart.append([13, 31])
    assert chart.lines() == [[0, 0, 0, 0, 13], [0, 0, 0, 0, 31]]

    chart.append([100])
    assert chart.lines() == [[0, 0, 0, 0, 100]]

    chart = LineChart(3)
    assert chart.lines() == [[0, 0, 0]]
    chart.append([10, 20])
    assert chart.lines() == [[0, 0, 10], [0, 0, 20]]
    chart.append([11, 22])
    assert chart.lines() == [[0, 10, 11], [0, 20, 22]]
    chart.append([44, 99])
    assert chart.lines() == [[10, 11, 44], [20, 22, 99]]
    chart.append([100, 200])
    assert chart.lines() == [[11, 44, 100], [22, 99, 200]]
