import win32api

# --------------------------------------------------------------------
# class DistanceCalculator
# fonction:
#     - Distance
# --------------------------------------------------------------------
class DistanceCalculator:
    def Distance(self, target, ref, method):
        param = '-sequences ' + target + ' ' + ref + ' -method ' + method + ' -result results -type character -parser csv'
        win32api.ShellExecute(0, 'open', 'MatchingToolBox.exe', param, '', 0)
