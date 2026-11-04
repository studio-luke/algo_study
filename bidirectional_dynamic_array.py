import operator


# A sequence backed by two dynamic arrays:
# logical order = reversed(front) + rear.
#
# Integer indexing takes O(1) time.
# End insertions and removals take amortized O(1) time.
# Rebalancing takes O(n) time and O(n) additional space.
class BDArray(object):
    def __init__(self, seq=()):
        # Materialize the input first so generators are also supported.
        self.front = []
        self.rear = list(seq)
        self.f_len = 0
        self.tot_len = len(self.rear)
        self._rebalance()

    def append_last(self, item):
        self.rear.append(item)
        self.tot_len += 1
        self._balance_if_needed()

    def append(self, item):
        self.append_last(item)

    def append_first(self, item):
        # Keep a single initial element in rear.
        if self.tot_len == 0:
            self.rear.append(item)
            self.f_len = 0
            self.tot_len = 1
            return

        # The end of front represents the beginning of the sequence.
        self.front.append(item)
        self.f_len += 1
        self.tot_len += 1
        self._balance_if_needed()

    def pop_last(self):
        if self.tot_len == 0:
            raise IndexError("pop from empty list")

        # A single element may be in front after reverse().
        if not self.rear:
            self._rebalance()

        item = self.rear.pop()
        self.tot_len -= 1
        self._balance_if_needed()
        return item

    def pop(self, i=-1):
        i = self._normalize_index(i)

        # Use dedicated end operations to avoid unnecessary shifting.
        if i == 0:
            return self.pop_first()
        if i == self.tot_len - 1:
            return self.pop_last()

        if i < self.f_len:
            # Convert the logical index into a reversed-front index.
            item = self.front.pop(self.f_len - i -1)
            self.f_len -= 1
        else:
            item = self.rear.pop(i - self.f_len)

        self.tot_len -= 1
        self._balance_if_needed()
        return item

    def pop_first(self):
        if self.tot_len == 0:
            raise IndexError("pop from empty list")

        # Delegate the single-element case regardless of its storage side.
        if self.tot_len == 1:
            return self.pop_last()
        elif not self.front:
            self._rebalance()

        self.tot_len -= 1
        self.f_len -= 1

        item = self.front.pop()
        self._balance_if_needed()
        return item

    def extend(self, seq):
        # Snapshot self-extension so iteration does not keep discovering
        # the newly appended elements.
        if seq is self:
            seq = list(self)

        for item in seq:
            self.append_last(item)

    def insert(self, i, item):
        # Accept integers and objects implementing __index__.
        i = operator.index(i)

        # Insertion positions are clamped rather than rejected.
        if i < 0:
            i += self.tot_len
        i = max(0, min(i, self.tot_len))

        if i == 0:
            self.append_first(item)
        elif i == self.tot_len:
            self.append_last(item)
        else:
            if i < self.f_len:
                # Insertion addresses a boundary between elements:
                # use f_len - i rather than f_len - i - 1.
                self.front.insert(self.f_len - i, item)
                self.f_len += 1
            else:
                self.rear.insert(i - self.f_len, item)

            self.tot_len += 1
            self._balance_if_needed()

    def clear(self):
        # Empty the existing backing lists and reset cached lengths.
        del self.front[:]
        del self.rear[:]
        self.f_len = 0
        self.tot_len = 0

    def remove(self, item):
        # Remove only the first matching element in logical order.
        for i in range(self.tot_len):
            if self[i] is item or self[i] == item:
                self.pop(i)
                return
        raise ValueError(f"{item} not in BDArray")

    def index(self, item, start=0, stop=None):
        start = operator.index(start)
        stop = self.tot_len if stop is None else operator.index(stop)

        # Normalize negative and out-of-range bounds.
        # The search includes start but excludes stop.
        start, stop, _ = slice(start, stop, 1).indices(self.tot_len)

        for i in range(start, stop):
            if self[i] is item or self[i] == item:
                # Return an index in the full sequence, not in the search range.
                return i

        raise ValueError(f"{item} not in BDArray")

    def count(self, item):
        count = 0
        for i in range(self.tot_len):
            if self[i] is item or self[i] == item:
                count += 1
        return count

    def reverse(self):
        # Reversing reversed(front) + rear gives reversed(rear) + front.
        # Swapping the backing lists therefore reverses the sequence in O(1).
        self.front, self.rear = self.rear, self.front
        self.f_len = len(self.front)

    def sort(self, *, key=None, reverse=False):
        # Sort a temporary list in logical order, then rebuild both halves.
        # This uses O(n) additional space even for already sorted input.
        data = self.front[::-1] + self.rear
        data.sort(key=key, reverse=reverse)

        mid = len(data) // 2
        self.front = data[:mid][::-1]
        self.rear = data[mid:]

        self.f_len = len(self.front)
        self.tot_len = len(data)

    def copy(self):
        # Create a new container while sharing the original element objects.
        return BDArray(self)

    def _rebalance(self):
        # Reconstruct logical order and split it approximately in half.
        # Store the first half in reverse order.
        data = self.front[::-1] + self.rear
        mid = len(data) // 2

        self.front = data[:mid][::-1]
        self.rear = data[mid:]

        self.f_len = len(self.front)
        self.tot_len = len(data)

    def _balance_if_needed(self):
        # Fewer than two elements cannot form two nonempty halves.
        if self.tot_len < 2:
            return

        f = len(self.front)
        r = len(self.rear)

        # Rebuild only when one side exceeds three times the other.
        # The near-even split after rebuilding prevents frequent rebuilds
        # during sequences of single-element insertions and removals.
        if 3 * f < r or 3 * r < f:
            self._rebalance()

    def _normalize_index(self, i):
        i = operator.index(i)

        if i < 0:
            i += self.tot_len

        # Access, assignment, and removal require an existing element.
        if not 0 <= i < self.tot_len:
            raise IndexError("Index out of range")

        return i

    def _order_compare(self, other, op):
        if not isinstance(other, (BDArray, list)):
            return NotImplemented

        # Lexicographic comparison: skip equal elements and compare
        # the first unequal pair using the requested operator.
        # Check identity first, including for shared NaN objects.
        for a, b in zip(self, other):
            if a is b or a == b:
                continue
            return op(a, b)

        # Equal prefixes are ordered by total length.
        return op(len(self), len(other))

    def __len__(self):
        return self.tot_len

    def __repr__(self):
        # Materializing logical order requires O(n) temporary space.
        return f"BDArray({self.front[::-1] + self.rear})"

    def __str__(self):
        return f"{self.front[::-1] + self.rear}"

    def __iter__(self):
        # Check the current length on each step so iteration can observe
        # appends made before the iterator is exhausted.
        i = 0
        while i < self.tot_len:
            yield self[i]
            i += 1

    def __contains__(self, item):
        for i in range(self.tot_len):
            if self[i] is item or self[i] == item:
                return True
        return False

    def __eq__(self, other):
        # Allow the other operand to handle unsupported comparisons.
        if not isinstance(other, (BDArray, list)):
            return NotImplemented

        if self.tot_len != len(other):
            return False

        for a, b in zip(self, other):
            if not (a is b or a == b):
                return False
        return True

    def __ne__(self, other):
        result = self.__eq__(other)

        # Propagate NotImplemented instead of interpreting it as a Boolean.
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        return self._order_compare(other, operator.lt)

    def __le__(self, other):
        return self._order_compare(other, operator.le)

    def __gt__(self, other):
        return self._order_compare(other, operator.gt)

    def __ge__(self, other):
        return self._order_compare(other, operator.ge)

    def __add__(self, other):
        if not isinstance(other, (BDArray, list)):
            return NotImplemented

        # Concatenation creates a new container.
        new_bda = BDArray(self)
        new_bda.extend(other)

        return new_bda

    def __iadd__(self, other):
        # In-place addition preserves object identity.
        self.extend(other)
        return self

    def __radd__(self, other):
        if not isinstance(other, (BDArray, list)):
            return NotImplemented

        # Preserve operand order for expressions such as list + BDArray.
        new_bda = BDArray(other)
        new_bda.extend(self)

        return new_bda

    def __mul__(self, n):
        try:
            n = operator.index(n)
        except TypeError:
            return NotImplemented

        new_bda = BDArray()
        if n <= 0 or self.tot_len == 0:
            return new_bda

        # Repeat references to the elements, not deep copies.
        for _ in range(n):
            new_bda.extend(self)

        return new_bda

    def __rmul__(self, n):
        return self.__mul__(n)

    def __imul__(self, n):
        try:
            n = operator.index(n)
        except TypeError:
            return NotImplemented

        # Multiplication by one needs neither copying nor rebuilding.
        if n == 1:
            return self

        if n <= 0 or self.tot_len == 0:
            self.front = []
            self.rear = []
            self.f_len = 0
            self.tot_len = 0
            return self

        # Snapshot once so each repetition uses only the original elements.
        original_data = list(self)
        for _ in range(n - 1):
            self.extend(original_data)

        return self

    def __getitem__(self, i):
        if isinstance(i, slice):
            # Normalize omitted bounds, negative indices, and negative steps.
            # A zero step raises ValueError.
            start, stop, step = i.indices(self.tot_len)

            # Copy only the selected elements into a new BDArray.
            return BDArray(
                [self[j] for j in range(start, stop, step)]
            )

        i = self._normalize_index(i)

        if self.f_len > i:
            return self.front[self.f_len - i - 1]
        else:
            return self.rear[i - self.f_len]

    def __setitem__(self, i, value):
        if not isinstance(i, slice):
            i = self._normalize_index(i)

            if i < self.f_len:
                self.front[self.f_len - i - 1] = value
            else:
                self.rear[i - self.f_len] = value
            return

        start, stop, step = i.indices(self.tot_len)

        # Snapshot incoming values to support iterables and self-assignment.
        # Copy replacement values rather than the whole existing sequence.
        values = list(value)
        positions = range(start, stop, step)
        k = len(positions)
        m = len(values)

        # Extended slices must preserve the selected element count.
        if step != 1:
            if m != k:
                raise ValueError(
                    f"attempt to assign sequence of size {m} "
                    f"to extended slice of size {k}"
                )

            for index, item in zip(positions, values):
                self[index] = item
            return

        # Equal-length replacement needs no shifting or rebalancing.
        if m == k:
            for index, item in zip(positions, values):
                self[index] = item
            return

        # An empty forward slice such as [5:2] inserts at start.
        stop = max(start, stop)
        f = self.f_len

        if stop <= f:
            # Map the logical interval to reversed-front coordinates.
            # Replacement values must also be reversed.
            self.front[f - stop:f - start] = values[::-1]

        elif start >= f:
            # The interval lies entirely within rear.
            self.rear[start - f:stop - f] = values

        else:
            # The interval crosses the boundary between the two arrays.
            # Remove its front portion and replace its rear portion.
            del self.front[:f - start]
            self.rear[:stop - f] = values

        # Refresh cached lengths after changing the sequence size.
        self.f_len = len(self.front)
        self.tot_len = self.f_len + len(self.rear)
        self._balance_if_needed()

    def __delitem__(self, i):
        if not isinstance(i, slice):
            self.pop(i)
            return

        start, stop, step = i.indices(self.tot_len)
        positions = range(start, stop, step)

        if len(positions) == 0:
            return

        # Preserve the original boundary while editing both arrays.
        f = self.f_len

        if step == 1:
            # Delete the part of the interval overlapping front.
            if start < f:
                front_stop = min(stop, f)
                del self.front[f - front_stop:f - start]

            # Delete the rear portion using the original boundary.
            if stop > f:
                rear_start = max(start, f)
                del self.rear[rear_start - f:stop - f]

        else:
            # Convert physical indices to logical indices and keep survivors.
            # Integer membership in range is checked arithmetically.
            #
            # This branch scans and rebuilds both arrays, even when few
            # elements are selected: O(n) time and O(n) additional space.
            self.front = [
                item
                for j, item in enumerate(self.front)
                if (f - j - 1) not in positions
            ]

            self.rear = [
                item
                for j, item in enumerate(self.rear)
                if (f + j) not in positions
            ]

        self.f_len = len(self.front)
        self.tot_len = self.f_len + len(self.rear)
        self._balance_if_needed()
        

"""
Initial version I wrote by my self.
It's a bidirectional dynamic array that supports amortized O(1) insert and delete operations at both ends.

"Doesn't support slicing, but supports indexing and iteration."
class BDArray:
    def __init__(self, seq=[]):
        if not hasattr(seq, '__len__') or not hasattr(seq, '__getitem__'):
            raise TypeError("Operand must be a sequence")
        
        if len(seq) == 0:
            self.front = list()
            self.rear = list()
        else:
            self.front = list()
            self.rear = list(seq)
            self.f_len = 0
            self.tot_len = len(seq)
            self.arrange()
        
    
    def arrange(self):
        if self.tot_len == 0:
            return

        new_f_len = self.tot_len // 2
        copy_BDA = list(self)
        for i in range(self.tot_len):
            if new_f_len > i:
                self.front.append(copy_BDA[new_f_len - i - 1])
            else:
                self.rear[i - new_f_len] = copy_BDA[i]
        if new_f_len < len(self.front):
            for _ in range(len(self.front) - new_f_len):
                self.front.pop()
        if self.tot_len - new_f_len < len(self.rear):
            for _ in range(len(self.rear) - (self.tot_len - new_f_len)):
                self.rear.pop()

        self.f_len = new_f_len

    def append_last(self, item):
        self.rear.append(item)
        self.tot_len += 1

    def append(self, item):
        self.append_last(item)

    def append_first(self, item):
        if self.tot_len == 0:
            self.rear.append(item)
            self.f_len = 0
            self.tot_len = 1
            return
        self.front.append(item)
        self.f_len += 1
        self.tot_len += 1

    def pop_last(self):
        if self.tot_len == 0:
            raise IndexError("pop from empty list")
        if not self.rear:
            self.arrange()
        self.tot_len -= 1
        if not self.rear:
            self.arrange()
        return self.rear.pop()

    def pop(self):
        return self.pop_last()

    def pop_first(self):
        if self.tot_len == 0:
            raise IndexError("pop from empty list")
        if self.tot_len == 1:
            return self.pop_last()
        elif not self.front:
            self.arrange()
        self.tot_len -= 1
        self.f_len -= 1
        return self.front.pop()

    def extend(self, seq):
        if not hasattr(seq, '__len__') or not hasattr(seq, '__getitem__'):
            raise TypeError("Operand must be a sequence")

        for item in seq:
            self.append_last(item)

    def __len__(self):
        return self.tot_len

    def __repr__(self):
        return f"BDArray({self.front[::-1] + self.rear})"

    def __str__(self):
        return f"{self.front[::-1] + self.rear}"

    def __iter__(self):
        for i in range(self.tot_len):
            yield self[i]  

    def __contains__(self, item):
        for i in range(self.tot_len):
            if self[i] == item:
                return True
        return False

    def __eq__(self, other):
        if not hasattr(other, '__len__') or not hasattr(other, '__getitem__'):
            return False
        if self.tot_len != len(other):
            return False
        for i in range(self.tot_len):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not hasattr(other, '__len__') or not hasattr(other, '__getitem__'):
            return False
        
        for i in range(min(self.tot_len, len(other))):
            if self[i] > other[i]:
                return False
            if self[i] < other[i]:
                return True
        return self.tot_len < len(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __add__(self, other):
        if not hasattr(other, '__len__') or not hasattr(other, '__getitem__'):
            raise TypeError("Operand must be a sequence")

        new_bda = BDArray(self)
        new_bda.extend(other)

        return new_bda

    def __mul__(self, n):
        if not isinstance(n, int):
            raise TypeError("Operand must be an integer")
        if n < 0:
            raise ValueError("Operand must be non-negative")

        new_bda = BDArray()
        for _ in range(n):
            new_bda.extend(self)

        return new_bda

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise TypeError("Index must be an integer")
        if i < 0 or i >= self.tot_len:
            raise IndexError("Index out of range")

        if self.f_len > i:
            return self.front[self.f_len - i - 1]
        else:
            return self.rear[i - self.f_len]


    def __setitem__(self, i, v):
        if not isinstance(i, int):
            raise TypeError("Index must be an integer")
        if i < 0 or i >= self.tot_len:
            raise IndexError("Index out of range")

        if self.f_len > i:
            self.front[self.f_len - i - 1] = v
        else:
            self.rear[i - self.f_len] = v
"""