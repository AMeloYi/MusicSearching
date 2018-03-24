import win32api

class DistanceCalculator:
    '''Class for calculating the distance between two objects
    Functions:
        Distance: Calculate the distance between two strings of vector
    '''

    def Distance(self, target, ref, method, result):
        '''Calculate the distance between two strings of vector

        This function can calculate the distance between two strings of vector. The
        target string of vectors is in the target file and the reference string of
        vectors is in the ref file. This function will directly call the 'exe' of
        the project 'MatchingToolBox'.

        Args:
            target: full path of the target file
            ref: full path of the reference file
            method: the method to calculate the distance between strings
            result: the name of the folder where user wants to save the results

        Returns:
            This function has no return. All the results will be saved in the files
            choosed by user.
        '''
        param = '-sequences ' + target + ' ' + ref + ' -method ' + method + ' -result ' + result + '-type character -parser csv'
        win32api.ShellExecute(0, 'open', 'MatchingToolBox.exe', param, '', 0)
