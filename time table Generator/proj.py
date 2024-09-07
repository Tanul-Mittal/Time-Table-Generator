import random
from tabulate import tabulate

def generate_timetable(courses, days, time_slots, class_duration):
    #Initialization of the dictionary
    timetable = {day: {slot: None for slot in time_slots} for day in days} 

    # Modify 12:00 PM time slot
    for day in timetable:
        timetable[day]['12:00 PM'] = {'course': 'Lunch Break', 'instructor': ''}
    
    for course, details in courses.items():
        credits = details['credits']
        instructors = details['instructors']
        is_lab = details.get('is_lab', False)
        for _ in range(credits):
            allocated = False
            while not allocated:
                day = random.choice(days)
                slot = random.choice(time_slots)
                # Check for consecutive slots for lab
                if is_lab and slot != '12:00 PM':
                    if slot != '3:00 PM':
                        next_slot = time_slots[(time_slots.index(slot) + 1) % len(time_slots)]
                        if next_slot != '3:00 PM' and timetable[day][slot] is None and timetable[day][next_slot] is None:
                            instructor = random.choice(instructors)
                            timetable[day][slot] = {'course': course, 'instructor': instructor}
                            timetable[day][next_slot] = {'course': course, 'instructor': instructor}
                            allocated = True
                    else:
                        prev_slot = time_slots[(time_slots.index(slot) - 1) % len(time_slots)]
                        if prev_slot != '2:00 PM' and timetable[day][slot] is None and timetable[day][prev_slot] is None:
                            instructor = random.choice(instructors)
                            timetable[day][slot] = {'course': course, 'instructor': instructor}
                            timetable[day][prev_slot] = {'course': course, 'instructor': instructor}
                            allocated = True
                # Check for non-lab slots
                elif timetable[day][slot] is None:
                    instructor = random.choice(instructors)
                    timetable[day][slot] = {'course': course, 'instructor': instructor}
                    allocated = True

    return timetable

# Rest of the code remains unchanged
def print_timetable_to_file(timetable):
    headers = ["Time Slots"] + list(timetable['Monday'].keys())
    rows = []

    for day, slots in timetable.items():
        row = [day]
        for details in slots.values():
            if details is not None:
                row.append(f"{details['course']}\n \n{details['instructor']}")
            else:
                row.append("Free")
        rows.append(row)

    with open("timetable.txt", "w") as f:
        f.write(tabulate(rows, headers=headers, tablefmt="grid"))

    print("Timetable written to timetable.txt")

    # User input for courses, credits, instructors, and class duration
courses = {}
while True:
    course_name = input("Enter course name (or 'exit' to finish): ")
    if course_name.lower() == 'exit':
        break

    credits = int(input(f"Enter credits for {course_name}: "))
    instructors = input(f"Enter instructors for {course_name} (comma-separated): ").split(',')
    is_lab = input(f"Is {course_name} a lab course? (yes/no): ").lower() == 'yes'
        
    courses[course_name] = {'credits': credits, 'instructors': instructors, 'is_lab': is_lab}

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
time_slots = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM']

class_duration = int(input("Enter class duration in minutes for non-lab courses: "))

timetable = generate_timetable(courses, days, time_slots, class_duration)
print_timetable_to_file(timetable)
