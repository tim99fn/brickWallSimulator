import os
import itertools

class Brick:
    def __init__(self, brick_id, x_llc, y_llc,x_urc,y_urc):
        self.id = brick_id
        self.position = (x_llc, y_llc,x_urc,y_urc)  # x, y coordinates (center or base)
        self.layed = False
        self.supporting_bricks = []  # IDs of bricks this brick rests on
        self.dimensions = (210, 62.5)  # default full brick size (length, height)


    def __repr__(self):
        return f"Brick(id={self.id}, pos={self.position}, layed={self.layed}, supports={self.supporting_bricks})"


class Wall:
    def __init__(self,bond, width_mm=2300, height_mm=2000):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.bricks = {}
        self.wall_visual = []
        self.bond=bond
        self._build_wall()
        
    # We'll now add a recursive function that simulates laying bricks in the envelope
# and recursively determines how many new bricks would become payable as a result.





    def build_english_cross_bond(self, width=2080,height=2300):
        #k=2n+1 x=n-2
        HALF_BRICK_LENGTH = 100
        BRICK_LENGTH = 210
        HEAD_JOINT = 10
        FULL_HALF_BRICK=110
        FULL_BRICK=220
        BED_JOINT = 12.5
        COURSE_HEIGHT = 62.5
        BRICK_CHAR = "░"
        JOINT_CHAR = " "
        num_courses = int(self.height_mm // COURSE_HEIGHT)
        brick_id=0
        
        number_small_bricks=int((self.width_mm-HALF_BRICK_LENGTH)/FULL_HALF_BRICK)
        number_even=int((self.width_mm-HALF_BRICK_LENGTH-FULL_BRICK)/FULL_BRICK)
        for course in range(num_courses):
            course_line = []
            x_llc=0
            y_llc=course*COURSE_HEIGHT
            x_urc=0
            y_urc = (course + 1) * COURSE_HEIGHT
            if course%4==0:
                x_urc = x_llc + BRICK_LENGTH+HEAD_JOINT
                course_line.append(BRICK_CHAR * 4 + JOINT_CHAR)
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                brick_id+=1
                x_llc=x_urc
                x_urc+=HALF_BRICK_LENGTH+HEAD_JOINT
                course_line.append(BRICK_CHAR * 2 + JOINT_CHAR)
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                x_llc=x_urc
                brick_id+=1
                for brick in range(number_even-1):

                    course_line.append(BRICK_CHAR * 4 + JOINT_CHAR)
                    x_urc = x_llc + BRICK_LENGTH+HEAD_JOINT
                    self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                    brick_id+=1
                    x_llc=x_urc

                x_urc = x_llc + BRICK_LENGTH
                course_line.append(BRICK_CHAR * 4 )
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc) 
                brick_id+=1
            elif course%2!=0:
                
                for brick in range(number_small_bricks):
                    x_urc = x_llc + FULL_HALF_BRICK
                    course_line.append(BRICK_CHAR * 2 + JOINT_CHAR)
                    self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                    brick_id+=1
                    x_llc=x_urc
                x_urc=x_llc+HALF_BRICK_LENGTH
                course_line.append(BRICK_CHAR * 2 )
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                brick_id+=1
            elif (course+2)%4==0:
                for brick in range(number_even):
                    course_line.append(BRICK_CHAR * 4 + JOINT_CHAR)
                    x_urc = x_llc + BRICK_LENGTH+HEAD_JOINT
                    self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                    brick_id+=1                   
                    x_llc=x_urc
                course_line.append(BRICK_CHAR * 2 + JOINT_CHAR)
                x_urc+=HALF_BRICK_LENGTH+HEAD_JOINT
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                brick_id+=1
                x_llc=x_urc
                x_urc = x_llc + BRICK_LENGTH
                course_line.append(BRICK_CHAR * 4)
                self.bricks[brick_id]=Brick(brick_id, x_llc, y_llc,x_urc,y_urc)   
                brick_id+=1
              
            self.wall_visual.append(course_line)
        self.assign_support()
        if course < num_courses - 1:
            self.wall_visual.append(JOINT_CHAR * (15 * 4 - 1))
                
    def assign_support(self):
        for brick in self.bricks.values():
            if brick.position[1]==0:
                brick.supports=[]
            else:
                bricks_in_below_course=[b for b in self.bricks.values() if b.position[3]==brick.position[1]]   
                for below in bricks_in_below_course:
                    horizontal_overlap_start = max(brick.position[0], below.position[0])
                    horizontal_overlap_end = min(brick.position[2], below.position[2])
                
                # A support exists if there's any horizontal overlap when vertically aligned
                    if horizontal_overlap_start < horizontal_overlap_end:
                        brick.supporting_bricks.append(below.id)
            
    def _build_wall(self):
        if self.bond=='stretcher':
            self.build_stretcher_wall()
        elif self.bond=='english_cross':
            self.width_mm=2080
            self.build_english_cross_bond()
    def build_stretcher_wall(self):
        HALF_BRICK_LENGTH = 100
        BRICK_LENGTH = 210
        HEAD_JOINT = 10
        BED_JOINT = 12.5
        COURSE_HEIGHT = 62.5

        bricks_per_course = int((self.width_mm - HALF_BRICK_LENGTH) // (BRICK_LENGTH + HEAD_JOINT))
        num_courses = int(self.height_mm // COURSE_HEIGHT)

        BRICK_CHAR = "░"
        JOINT_CHAR = " "

        for course in range(num_courses):
            course_line = []
            x_llc=0
            y_llc=course*COURSE_HEIGHT
            x_urc=0
            y_urc = (course + 1) * COURSE_HEIGHT
            if course % 2 == 0:
                course_line.append(BRICK_CHAR * 2 + JOINT_CHAR)
                for brick in range(bricks_per_course):
                    x_urc = HALF_BRICK_LENGTH + HEAD_JOINT + brick * (BRICK_LENGTH + HEAD_JOINT)
                    

                    brick_id = course * (bricks_per_course+1) + brick
                    new_brick = Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                    x_llc=x_urc
                    if course > 0:
                        if brick ==0:
                            new_brick.supporting_bricks = [brick_id-11]
                        else:
                            new_brick.supporting_bricks=[brick_id-12,brick_id-11]

                    self.bricks[brick_id] = new_brick
                    course_line.append( BRICK_CHAR * 4 + JOINT_CHAR)
                # End cap
                end_brick_id = (course + 1) * (bricks_per_course+1)-1
                x_urc = x_llc + BRICK_LENGTH
                y = (course + 1) * COURSE_HEIGHT
                new_brick=Brick(end_brick_id, x_llc, y_llc,x_urc,y_urc)
                if course==0:
                    new_brick.supporting_bricks=[]
                else:
                    new_brick.supporting_bricks=[end_brick_id-12,end_brick_id-11]
                self.bricks[end_brick_id] = new_brick
            else:
                for brick in range(bricks_per_course):
                    x_urc = (brick + 1) * (BRICK_LENGTH + HEAD_JOINT)

                    brick_id = course * (bricks_per_course+1) + brick
                    new_brick = Brick(brick_id, x_llc, y_llc,x_urc,y_urc)
                    x_llc=x_urc
                    if course > 0:
                        new_brick.supporting_bricks = [brick_id-11,brick_id-10]

                    else:
                        new_brick.layable=True
                    self.bricks[brick_id] = new_brick
                    course_line.append( BRICK_CHAR * 4 + JOINT_CHAR)
                course_line.append(BRICK_CHAR * 2 + JOINT_CHAR)
                end_brick_id = (course + 1) * (bricks_per_course+1)-1
                x_urc = x_llc + HALF_BRICK_LENGTH

                new_brick=Brick(end_brick_id, x_llc, y_llc,x_urc,y_urc)
                if course==0:
                    new_brick.supporting_bricks=[]
                else:
                    new_brick.supporting_bricks=[end_brick_id-11]
                self.bricks[end_brick_id] = new_brick
                

            self.wall_visual.append(course_line)
            if course < num_courses - 1:
                self.wall_visual.append(JOINT_CHAR * (bricks_per_course * 4 - 1))

    def _get_supporting_ids(self, course, brick_index, bricks_per_course):
        # Simple support: find bricks below within same x-span
        supporting_ids = []
        below_course = course - 1
        for b_id, brick in self.bricks.items():
            if int(b_id) // bricks_per_course == below_course:
                bx, by = brick.position
                cx = (brick_index + 1) * (210 + 10)  # approx horizontal span
                if abs(bx - cx) < 210:
                    supporting_ids.append(b_id)
        return supporting_ids

    def find_bricks_in_envelope(self, initial_position, width=800, height=1300):
        # Envelope defines a rectangular area
        envelope_llx = initial_position[0]
        envelope_lly = initial_position[1]
        envelope_urx = envelope_llx + width
        envelope_ury = envelope_lly + height

        bricks_in_envelope = []
        for brick in self.bricks.values():
            # Get brick's bounding box coordinates
            brick_llx, brick_lly, brick_urx, brick_ury = brick.position

            # Check for overlap between brick's bounding box and envelope's bounding box
            # Overlap in X-axis: max(start_x1, start_x2) < min(end_x1, end_x2)
            # Overlap in Y-axis: max(start_y1, start_y2) < min(end_y1, end_y2)

            if brick_llx>=envelope_llx and brick_lly>=envelope_lly and brick_urx<=envelope_urx and brick_ury<=envelope_ury:
                bricks_in_envelope.append(brick)

            # If there's overlap in both dimensions, the brick is in the envelop
        return bricks_in_envelope
    def get_envelopes_with_layable_bricks(self, step_x=100, step_y=62.5, width=800, height=1300):
        envelopes_with_payable = []
        nx = int((self.width_mm) / step_x )
        ny = int((self.height_mm) / step_y)

        for xi in range(nx):
            for yi in range(ny):
                x = xi * step_x
                y = yi * step_y
                bricks_in_env = self.find_bricks_in_envelope((x, y), width, height)

                for brick in bricks_in_env:
                    if brick.layed:
                        continue
                    # Payable if course 0 (no supports) or all supports are laid
                    if not brick.supporting_bricks or all(self.bricks[sid].layed for sid in brick.supporting_bricks):
                        envelopes_with_payable.append([xi, yi])
                        break  # No need to check other bricks in this envelope

        return envelopes_with_payable
     
    def recursively_count_payable_bricks(self, initial_position, width=800, height=1300):
        """
        Recursively count the number of bricks that could be laid if we lay all currently layable ones.
        Does not change actual layed state.
        """
        # Clone current layed state to restore later
        original_layed = {brick.id: brick.layed for brick in self.bricks.values()}

        # Set to keep track of all hypothetically layed bricks
        simulated_layed = []

        # Step 1: Find layable bricks in the initial envelope
        bricksInEnvelope = self.find_bricks_in_envelope(initial_position, width, height)
        layableBricksInEnvelope=[b for b in bricksInEnvelope if b.layed==False]
        frontier=[b for b in layableBricksInEnvelope if b.supporting_bricks==[]or all(self.bricks[s].layed for s in b.supporting_bricks) ]
        while frontier:
            new_frontier = []

            for brick in frontier:
                brick.layed = True
                simulated_layed.append(brick.id)

            # Update layable status for other bricks based on new state
            for brick in layableBricksInEnvelope:
                if not brick.layed and all(self.bricks[s].layed for s in brick.supporting_bricks):
                    new_frontier.append(brick)

            frontier = new_frontier

        # Restore the original layed state
        for brick_id, was_layed in original_layed.items():
            self.bricks[brick_id].layed = was_layed

        return len(simulated_layed),simulated_layed
    def find_best_multi_stride_path(self, lookahead_remaining, step_x, step_y, width, height):
        """
        Recursively finds the best sequence of strides for a given lookahead depth.
        Returns the total bricks laid in the best path and the IDs of the first stride.
        """
        if lookahead_remaining == 0:
            return {'total_bricks': 0, 'first_stride_ids': []} # Base case

        # Save the original 'layed' state of all bricks before simulation
        original_layed_state = {brick.id: brick.layed for brick in self.bricks.values()}

        overall_best_total_bricks = -1
        best_first_stride_ids_for_path = []

        potential_first_envelopes = self.get_envelopes_with_layable_bricks(step_x, step_y, width, height)

        if not potential_first_envelopes:
            return {'total_bricks': 0, 'first_stride_ids': []} # No possible first strides

        for envelope_coords in potential_first_envelopes:
            # Simulate laying the first stride from this envelope
            first_stride_count, first_stride_ids = self.recursively_count_payable_bricks(envelope_coords, width, height)

            if not first_stride_ids:
                # If this envelope doesn't yield any layable bricks immediately, skip it
                continue

            current_path_total_bricks = first_stride_count

            # Temporarily apply the first stride to the wall's state for subsequent recursive calls
            for brick_id in first_stride_ids:
                self.bricks[brick_id].layed = True

            # Recursively find the best path for the remaining lookahead from this new state
            subsequent_result = self.find_best_multi_stride_path(
                lookahead_remaining - 1,
                step_x,
                step_y,
                width,
                height
            )
            current_path_total_bricks += subsequent_result['total_bricks']

            # Restore the original 'layed' state for all bricks before processing the next potential first stride
            for brick_id, was_layed in original_layed_state.items():
                self.bricks[brick_id].layed = was_layed

            # If this path is better, update the overall best
            if current_path_total_bricks > overall_best_total_bricks:
                overall_best_total_bricks = current_path_total_bricks
                best_first_stride_ids_for_path = first_stride_ids
            # Tie-breaking: if counts are equal, prefer path with fewer bricks in the first stride (more efficient)
            elif current_path_total_bricks == overall_best_total_bricks and len(first_stride_ids) < len(best_first_stride_ids_for_path):
                best_first_stride_ids_for_path = first_stride_ids


        return {'total_bricks': overall_best_total_bricks, 'first_stride_ids': best_first_stride_ids_for_path}
    def greedy_laying_strategy(self, step_size_x=220 , step_size_y=62.5, width=800, height=1300):
        full_lay_order=[]
        while True:
            all_bricks_laid = all(brick.layed for brick in self.bricks.values())
            if all_bricks_laid:
                print("All bricks have been laid. Stopping the greedy strategy.")
                break

            test_envelopes = self.get_envelopes_with_layable_bricks(step_size_x,step_size_y)
            if not test_envelopes:
                print("No more layable envelopes found. Stopping the greedy strategy.")
                break

            best_count = -1
            lay_ids = []

            for envelope_coords in test_envelopes:
                # Convert envelope coordinates back to pixel coordinates for recursively_count_payable_bricks
                x = envelope_coords[0] * step_size_x
                y = envelope_coords[1] * step_size_y
                count, ids = self.recursively_count_payable_bricks((x, y), width, height)

                if count >= best_count:
                    best_count = count
                    lay_ids = ids
            
            if not lay_ids:  # If no new bricks can be laid in this iteration
                print("No new bricks can be laid in this iteration. Stopping the greedy strategy.")
                break
  
            for brick_id in lay_ids:
                self.bricks[brick_id].layed = True  
            full_lay_order.append(lay_ids)            

        return full_lay_order # Return all laid brick IDs
 
                


    def print_wall(self):
        for line in reversed(self.wall_visual):
            print(''.join(line))





    def interactive_laying(self):
        colors = ["█", "▓", "■", "□", "▲", "▼", "◆", "◇", "●", "○"]
        color_cycle = itertools.cycle(colors) # Create an infinite cycle of colors

        all_steps = self.greedy_laying_strategy()
        print(len(all_steps))
        #bricks_to_lay = [brick_id for step in all_steps for brick_id in step]
        for stride in all_steps:
            stride_color=next(color_cycle)
            for brick_id in stride:
                self.bricks[brick_id].layed = True
                course=int(brick_id/11)*2


                brick_number=brick_id%11
            
                
                #course=self.wall_visual[course]
                #course[brick_number]=course[brick_number].replace('░', '█')
                self.wall_visual[course][brick_number]=self.wall_visual[course][brick_number].replace('░', stride_color)
                #self.wall_visual[course]=course
                input("Press Enter to lay next brick...")
                self.print_wall()

        print("✅ All bricks laid!")



wall = Wall(bond='english_cross',width_mm=2080)
wall.interactive_laying()

# Run interactive laying
#interactive_laying(wall)
# Simulate laying a few base bricks


# Run recursive hypothetical simulation


