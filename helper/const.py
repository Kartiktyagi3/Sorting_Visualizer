#color scheme
bg_color = '#68b0ab'
processing_color = '#faf3dd'
pivot_color = '#4a7c59'
array_color = '#c8d5b9'
array_outline = '#4a7c59'

#canvas size
canvas_width = 975
canvas_height = 543
size_array = 160

#Multipliers and space between consecutive lines
width_scaling = int(((canvas_width)//(size_array)))
height_scaling = 4  # unit length of the array=10 px
distance_in_two = width_scaling + 2
height_limit = canvas_height//height_scaling
