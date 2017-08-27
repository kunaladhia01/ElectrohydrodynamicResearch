#Kunal Adhia
#8/10/17

'''
Finds threshold Ef for droplet w/ elecrtode above
Contact angle = 45 degrees
Rb = 0.4
Refine = 8
Cmu = 0.1
Q = 20
'''

import os

input_file = 'electro.gfs'

def run_command(x):
	# gerris2D command for Ef = x
	return 'gerris2D -DEf=' + str(Ef) + ' electro.gfs'

def droplet_reaches_electrode():
	
	# parse through interface-%ld.gfs files, find interface coordinates, save h(t), t	
	step = 0
	while True:
		try:
			file_to_open = 'interface-' + str(step) + '.gfs'
			f = open(file_to_open, 'r')

			first_line = True
			coord = []
			for line in f:
				
				#ignore first line
				if first_line:
					first_line = False
					continue

				# search for 0 < T  < 1 (boundary)
				copy = line + ' '
				for i in range(3):
					copy = copy[copy.index(' ')+1:]

				# add boundary x-coord to list
				if copy[1] == '.': 
					coord.append(-1.0*float(line[:line.index(' ')]))

			f.close()
			min_x = min(coord) # |x| of droplet peak
			height = 0.50 - min_x # height of droplet

			#save height
			f = open('height.txt', 'a')
			f.write(str(height) + '\n')
			f.close()

			#save time
			time_file = 'result-' + str(step) + '.gfs'
			f = open(time_file, 'r')
	
			for i in range(15):
				line = f.readline()

			time_line = f.readline()
			time_line = time_line[time_line.index('t')+4:]
			time_line = float(time_line[:time_line.index(' ')])
			f.close()

			f = open('time.txt', 'a')
			f.write(str(time_line) + '\n')
			f.close()

			# quit if electrode reached
			if min_x < 0.18:
				return True
			
			# next output
			step += 100

		except:
			break

	return False



if __name__ == '__main__':

	#Try different Ef's
	threshold = -1
	for i in range(1000, 4100, 100): # Ef from .275 to 0.281, step = 0.005

		Ef = i / 10000.0
		print Ef	
		#os.system('rm result*.gfs')
	
		#run simulation
		os.system(run_command(Ef))

		# format: folder, __[Ef]
		new_folder = 'mkdir __' + str(Ef)
		os.system(new_folder)

		#create t, h(t) files
		f = open('time.txt', 'w+')
		f.close()
		f = open('height.txt', 'w+')
		f.close()

		# postprocessing
		move_on = droplet_reaches_electrode()
	
		# move to subdir, clear . dir
		move_everything = 'mv result*.gfs interface*.gfs time.txt height.txt __' + str(Ef)
		os.system(move_everything)

		threshold = Ef
		
	# save threshold value
	f = open('threshold.txt', 'w+')
	f.write(str(threshold))
	f.close()


