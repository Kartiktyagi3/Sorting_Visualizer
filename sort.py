from tkinter import *
from tkinter import ttk
from time import sleep
from helper.const import * 
import random
import threading

class Display:

    def __init__(self):
        self.array = []
        self.background = w.create_rectangle(
            0, 0, canvas_width, canvas_height, fill=bg_color)
        self.array_visual = []
        self.speed = [0.0025, 0.01, 0.03, 0.1, 0.2]
        self.speed_index = 1
        self.initialize_array()

    #randomly initialize an array
    def initialize_array(self):
        w.delete('all')
        self.background = w.create_rectangle(
            0, 0, canvas_width, canvas_height, fill=bg_color)
        for i in range(size_array):
            self.array.append(random.randint(1, height_limit))
            self.array_visual.append(w.create_line((i+2)*width_scaling, canvas_height, (
                i+2)*width_scaling, canvas_height-self.array[i]*height_scaling, width=width_scaling, fill=array_color))

    def process_item(self, index, fill_color=processing_color):
        w.itemconfig(self.array_visual[index], fill=fill_color)

    def display_item(self, index):
        w.delete(self.array_visual[index])
        self.array_visual[index] = w.create_line((index+2)*width_scaling, canvas_height, (
            index+2)*width_scaling, canvas_height-self.array[index]*height_scaling, width=width_scaling, fill=array_color)

    def visual_swap(self, i, j):
        self.process_item(i)
        self.process_item(j)
        self.array[i], self.array[j] = self.array[j], self.array[i]
        w.coords(self.array_visual[i], (i+2)*width_scaling, canvas_height,
                 (i+2)*width_scaling, canvas_height-self.array[i]*height_scaling)
        w.coords(self.array_visual[j], (j+2)*width_scaling, canvas_height,
                 (j+2)*width_scaling, canvas_height-self.array[j]*height_scaling)
        self.display_item(i)
        self.display_item(j)


class Sort(Display):

    def __init__(self):
        super().__init__()
        self.array_in_use=False

    def speed_zero(self):
        self.speed_index=0

    def randomize_array(self):
        del self.array[:]
        del self.array_visual[:]
        self.initialize_array()

    def insertion_sort(self):
        for i in range(size_array):
            for j in range(i, 0, -1):
                if self.array[j] < self.array[j-1]:
                    self.array[j], self.array[j-1] = self.array[j-1], self.array[j]
                    if self.speed_index!=0:
                        self.process_item(j)
            if self.speed_index != 0:
                for j in range(i, -1, -1):
                    self.display_item(j)
        if self.speed_index == 0:
            for i in range(size_array):
                self.display_item(i)
        self.array_in_use = False

    def merge(self, A, B, start, end):
        C = []
        i, j = 0, 0
        for item in range(start, end):
            self.process_item(item)
        sleep(self.speed[self.speed_index])
        while (i < len(A) and j < len(B)):
            if A[i] <= B[j]:
                C.append(A[i])
                i += 1
            else:
                C.append(B[j])
                j += 1
        while (i < len(A)):
            C.append(A[i])
            i += 1
        while (j < len(B)):
            C.append(B[j])
            j += 1

        main_array_index = start
        for i, item in enumerate(C):
            self.array[main_array_index] = item
            self.display_item(main_array_index)
            main_array_index += 1
        sleep(self.speed[self.speed_index])
        return C

    def merge_sort_divide(self, A, start, end):
        if len(A) == 1:
            return A
        else:
            mid = (len(A))//2
            left_half = self.merge_sort_divide(A[:mid], start, start+mid)
            right_half = self.merge_sort_divide(A[mid:], start+mid, end)
            return self.merge(left_half, right_half, start, end)

    def merge_sort(self, start, end):
        self.merge_sort_divide(self.array, start, end)
        self.array_in_use = False

    def quick_sort(self):
        self.quick_sort_helper(0,size_array-1)
        self.array_in_use = False

    def quick_sort_helper(self, startIndex, endIndex):
        if startIndex >= endIndex:
            return
        pivot = random.randint(startIndex, endIndex)
        self.visual_swap(pivot, startIndex)
        pivot = startIndex
        leftIndex, rightIndex, pivotValue = startIndex + \
            1, endIndex, self.array[pivot]
        self.process_item(pivot, pivot_color)
        while leftIndex <= rightIndex:
            self.process_item(leftIndex)
            self.process_item(rightIndex)
            if self.array[leftIndex] > pivotValue and self.array[rightIndex] < pivotValue:
                self.visual_swap(leftIndex, rightIndex)
                sleep(self.speed[self.speed_index])
            self.display_item(leftIndex)
            self.display_item(rightIndex)
            if self.array[leftIndex] <= pivotValue:
                leftIndex += 1
            if self.array[rightIndex] >= pivotValue:
                rightIndex -= 1

        self.visual_swap(rightIndex, pivot)

        #chech which subarray is smaller
        if (rightIndex-1)-startIndex < endIndex-(rightIndex+1):
            self.quick_sort_helper(startIndex, rightIndex-1)
            self.quick_sort_helper(rightIndex+1, endIndex)
        else:
            self.quick_sort_helper(rightIndex+1, endIndex)
            self.quick_sort_helper(startIndex, rightIndex-1)


    def heap_sort(self):
        #Creating a heap out of the array
        for i in range(len(self.array)//2, -1, -1):
            self.max_heapify(i)
        sleep(self.speed[self.speed_index])
        #Shifting the max element to the heap_size index of the array
        #decrease heap_size by 1 after each itteration
        heap_size = len(self.array)
        for i in range(len(self.array)):
            sleep(self.speed[self.speed_index])
            self.visual_swap(0, heap_size-1)
            heap_size -= 1
            self.max_heapify(0, heap_size)
        self.array_in_use = False

    def max_heapify(self, index, heap_size=size_array):
        left_child = 2*index+1
        right_child = 2*index+2

        if left_child < heap_size and self.array[left_child] > self.array[index]:
            largest = left_child
        else:
            largest = index
        if right_child < heap_size and self.array[right_child] > self.array[largest]:
            largest = right_child

        if largest != index:
            self.visual_swap(largest, index)
            self.max_heapify(largest, heap_size)

    def count_sort(self):
        universal_set = int(((canvas_height-1)/(height_scaling))+1)
        A = [0]*universal_set
        sleep(self.speed[self.speed_index])
        for i, item in enumerate(self.array):
            A[item] += 1
            self.process_item(i)
        sleep(self.speed[self.speed_index])

        # itter for itterating through the main array
        itter = 0
        for i, item in enumerate(A):
            if item == 0:
                continue
            while item > 0:
                sleep(self.speed[self.speed_index])
                self.array[itter] = i
                self.display_item(itter)
                itter += 1
                item -= 1
        self.array_in_use=False

    def radix_sort(self):
        max_item=max(self.array)
        exp=1
        while max_item//exp>0:
            self.radix_count_helper(exp)
            exp*=10

    def radix_count_helper(self,exp):
        A=[0]*size_array
        count=[0]*10
        
        for i,item in  enumerate(self.array):
            index= item//exp
            count[index%10]+=1

        self.process_item(count[0]-1)
        for i in range(1,10):
            count[i]+=count[i-1]
            self.process_item(count[i]-1)
        sleep(self.speed[self.speed_index])

        #for stability of sort this is run backword
        for i in reversed(range(0,len(self.array))):
            index=self.array[i]//exp
            #To adjust for 0 based indexing
            A[count[index%10]-1]=self.array[i]
            count[index%10]-=1


        for i,item in enumerate(A):
            sleep(self.speed[self.speed_index])
            self.array[i]=item
            self.display_item(i)
        


def background(func, *args):
    global thread
    if not thread.is_alive():
        T.speed_index=1
        thread = threading.Thread(target=func, args=args, daemon=True)
        thread.start()


if __name__ == "__main__":
    #Tkinter screen widget 
    root = Tk()
    root.title('Sorting Visualiser')

    #create instance of Canvas
    w = Canvas(root, width=canvas_width, height=canvas_height)

    #create instance of Sort Class
    T = Sort()
    thread=threading.Thread()

    #create Various buttons to be used on screen
    speed_up_button = Button(root, text='Speed Up',
                        command=lambda: T.speed_zero())
    sort_insertion = Button(root, text='Insertion Sort',
                            command=lambda: background(T.insertion_sort))
    sort_merge = Button(root, text='Merge Sort',
                        command=lambda: background(T.merge_sort, 0, size_array))
    sort_quick = Button(root, text='Quick Sort',
                        command=lambda: background(T.quick_sort))
    sort_heap = Button(root, text='Heap Sort',
                    command=lambda: background(T.heap_sort))
    sort_count = Button(root, text='Count Sort',
                        command=lambda: background(T.count_sort))
    randomize_array = Button(root, text='randomize',
                             command=lambda:background(T.randomize_array))
    sort_radix = Button(root, text='Radix Sort',
                        command=lambda: background(T.radix_sort))

    '''
    complete_button = Button(root, text='complete',
                            command=lambda: T.change_speed(0))
    '''
    #placement of thing on screen

    w.grid(row=0, column=0, columnspan=9)
    speed_up_button.grid(row=1, column=0)
    randomize_array.grid(row=1, column=2)
    sort_insertion.grid(row=1, column=3)
    sort_merge.grid(row=1, column=4)
    sort_quick.grid(row=1, column=5)
    sort_heap.grid(row=1, column=6)
    sort_count.grid(row=1, column=7)
    sort_radix.grid(row=1,column=8)
    root.after(10, w.update_idletasks())
    '''
    complete_button.grid(row=1, column=1)
    '''
    #magical graphics
    root.mainloop()
