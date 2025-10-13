forest_map = [
 [1,0,0,0,1],
 [1,0,1,1,1],
 [1,1,0,1,1],
 [1,0,1,1,0],
 [0,1,0,1,1]
]

m = 3                
center = (2, 3)      
r, c = center

start_row = r - m//2     
end_row   = r + m//2 + 1 
start_col = c - m//2   
end_col   = c + m//2 + 1

zone=[ row[start_col:end_col] for row in forest_map[start_row:end_row] ]
print(zone)

