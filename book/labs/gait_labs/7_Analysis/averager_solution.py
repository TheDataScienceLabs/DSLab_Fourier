"""
This provides the class Averager,
which is suitable for both Python and Micropython.
This also contains tests for the class, which will
allow us to see what features are missing.
"""

class Averager:
    """Accepts inputs and stores them in a list. Once
    the predetermined length is met, it writes over the
    oldest value.
    
    Parameters
    ----------
    length: int
        how many values to store
        
    Examples
    --------
    give the average of four readings
    >>> avg = Averager(4)
    >>> for x in range(2, 6):
    ...     avg.append(x)
    >>> avg.get()
    3.5
    
    follow the behavior step-by-step:
    >>> avg = Averager(2)
    >>> avg.append(3)
    
    if we ask for the average before the list is full, we get nan
    >>> avg.get()
    nan
    
    the list is not full yet
    >>> avg.list
    [3, nan]
    
    we are ready to put the next thing at position 1
    >>> avg.index
    1
    >>> avg.append(5)
    
    now that it's full, we can get the average
    >>> avg.get()
    4.0
    
    we are back to pointing at position 0
    >>> avg.index
    0
    
    if we add new data, the oldest gets written over
    >>> avg.append(10)
    >>> avg.get()
    7.5
    >>> avg.list
    [10, 5]
    >>> avg.index
    1
    
    We could even have an averager with one value, though it might not be particularly useful.
    >>> avg = Averager(1)
    >>> for x in range(1001):
    ...    avg.append(x)
    >>> avg.get()
    1000.0
    
    """
    
    def __init__(self, length):
        self.list = [float('nan')] * length
        self.index = 0
        
    def append(self, x):
        """Put a new value in the list at the current index,
        and increment the index (looping back to zero if necessary)
        
        Parameters
        ----------
        x: float
            the number to put into the list.
        """
        self.list[self.index] = x
        self.index += 1
        self.index %= len(self.list)
        
    def get(self):
        """Find the average of all the numbers in the list and return it.
        
        Returns
        -------
        float:
            the average of all the items in the list.
        """
        return sum(self.list)/len(self.list)