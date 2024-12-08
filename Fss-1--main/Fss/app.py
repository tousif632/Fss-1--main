from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Routine generator logic
def output(intensity):
    listt = []

    def cooldown():
        cooldown_exercises = [
            ["Standing Forward Bend", (1, 2)],
            ["Seated Hamstring Stretch", (1, 2)],
            ["Butterfly Stretch", (1, 2)],
            ["Cat-Cow Stretch", (2, 3)],
            ["Child's Pose", (2, 3)],
            ["Shoulder Stretch", (1, 2)],
            ["Triceps Stretch", (1, 2)],
            ["Chest Stretch", (1, 2)],
            ["Figure Four Stretch", (2, 3)],
            ["Calf Stretch", (2, 3)],
            ["Side Stretch", (1, 2)],
            ["Wrist Stretch", (1, 1)],
            ["Neck Stretch", (1, 1)],
            ["Hip Flexor Stretch", (2, 3)],
            ["Deep Breathing", (1, 1)]
        ]

        max_intensity = intensity // 5
        current_sum = 0

        for exercise, rep_range in cooldown_exercises:
            current_sum += 1  # Each cooldown exercise counts as one in the total
            if max_intensity > current_sum:
                reps = random.randint(*rep_range)
                listt.append(f"{exercise} - {reps} reps")
            else:
                break

    def exercises():
        exercises = [
            ["Jogging in Place", (8, 12)],
            ["Burpees", (6, 10)],
            ["High Knees", (8, 12)],
            ["Jump Squats", (6, 10)],
            ["Push-Ups", (6, 10)],
            ["Plank to Downward Dog", (6, 8)],
            ["Mountain Climbers", (10, 15)],
            ["Lateral Bounds", (8, 12)],
            ["Walking Lunges", (8, 12)],
            ["T-Push-Ups", (6, 10)],
            ["Single-Leg Deadlifts", (8, 12)],
            ["Box Jumps", (6, 10)],
            ["Plank Jacks", (8, 12)],
            ["Skater Jumps", (8, 12)],
            ["Burpee Broad Jumps", (6, 10)],
            ["Side Lunges", (8, 12)],
            ["Russian Twists", (10, 15)],
            ["Bear Crawls", (8, 12)],
            ["Frog Jumps", (6, 10)],
            ["V-Ups", (10, 15)],
            ["Kettlebell Swings", (8, 12)],
            ["Medicine Ball Slams", (6, 10)],
            ["Jumping Jacks", (15, 20)],
            ["Inchworms", (8, 12)],
            ["Plank Shoulder Taps", (10, 15)],
            ["Squat Jumps", (6, 10)],
            ["Single-Arm Rows", (8, 12)]
        ]

        max_intensity = intensity * 0.6
        current_sum = 0

        for exercise, rep_range in exercises:
            current_sum += 1  # Each exercise counts as one in the total
            if max_intensity > current_sum:
                reps = random.randint(*rep_range)
                listt.append(f"{exercise} - {reps} reps")
            else:
                break

    def warmup():
        warmup_exercises = [
            ["Jumping Jacks", (10, 20)],
            ["High Knees", (10, 15)],
            ["Arm Circles", (8, 12)],
            ["Leg Swings", (8, 12)],
            ["Lunges", (10, 15)],
            ["Butt Kicks", (10, 15)],
            ["Dynamic Stretching", (5, 10)],
            ["Mountain Climbers", (10, 15)],
            ["Inchworms", (8, 12)],
            ["Bodyweight Squats", (10, 15)],
            ["Hip Circles", (8, 12)],
            ["Side Shuffles", (10, 15)],
            ["Bear Crawls", (8, 12)],
            ["Ankle Hops", (8, 12)],
            ["Toe Touches", (5, 10)]
        ]

        max_intensity = intensity // 5
        current_sum = 0

        for exercise, rep_range in warmup_exercises:
            current_sum += 1  # Each warmup exercise counts as one in the total
            if max_intensity > current_sum:
                reps = random.randint(*rep_range)
                listt.append(f"{exercise} - {reps} reps")
            else:
                break

    warmup()
    exercises()
    cooldown()

    return listt

# Function to calculate BMI and adjust intensity
def calculate_intensity(weight, height):
    # Convert height from cm to meters
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)

    # Map BMI to intensity (you can adjust this mapping as needed)
    if bmi < 18.5:
        return 50  # Low intensity for underweight
    elif 18.5 <= bmi < 24.9:
        return 70  # Moderate intensity for normal weight
    elif 25 <= bmi < 29.9:
        return 60  # Moderate intensity for overweight
    else:
        return 40  # Lower intensity for obesity

# Flask routes
@app.route('/gen')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    intensity = calculate_intensity(weight, height)
    routine = output(intensity)
    return render_template('index.html', routine=routine)

@app.route("/")
def diet():
    return render_template("Home.html")

class WeeklyDietPlan:
    def __init__(self, age, height, weight, goal, duration, diet_type, gender, activity_level):
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal
        self.duration = duration
        self.diet_type = diet_type
        self.gender = gender
        self.activity_level = activity_level
        self.bmr = self.calculate_bmr()
        self.daily_calories = self.adjust_calories()
        self.plan = self.create_diet_plan()

    def calculate_bmr(self):
        if self.gender == 'male':
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def adjust_calories(self):
        if self.goal == 'weight gain':
            return self.bmr + 500
        elif self.goal == 'weight loss':
            return self.bmr - 500
        else:
            return self.bmr  # Maintenance

    def create_diet_plan(self):
        if self.diet_type == 'weight gain':
            return {f'Day {i+1}': self.get_weight_gain_plan(i+1) for i in range(7)}
        elif self.diet_type == 'weight loss':
            return {f'Day {i+1}': self.get_weight_loss_plan(i+1) for i in range(7)}
        else:
            return {}

    def get_weight_gain_plan(self, day):
        # Adjust quantities based on daily caloric needs
        return {
            'Breakfast (Pre-Workout)': [
                f'{self.adjust_meal_amount(6)} slices whole wheat bread',
                f'{self.adjust_meal_amount(4)} whole eggs',
                f'{self.adjust_meal_amount(1)} cup oats with milk and honey',
                '1 banana'
            ],
            'Mid-Morning (Snack)': [
                '1 scoop whey protein with milk',
                f'{self.adjust_meal_amount(1)} slice whole wheat bread with peanut butter',
                f'{self.adjust_meal_amount(6)} almonds'
            ],
            'Lunch (High Protein)': [
                f'{self.adjust_meal_amount(250)}g chicken breast or paneer',
                f'{self.adjust_meal_amount(250)}g cooked rice',
                'Steamed veggies',
                'Sambar'
            ],
            'Afternoon Snack': [
                'Green tea or black coffee',
                '1 small handful of mixed nuts',
                '1 boiled egg'
            ],
            'Dinner': [
                f'{self.adjust_meal_amount(150)}g chicken breast or paneer',
                'Steamed veggies',
                f'{self.adjust_meal_amount(2)} chapatis',
                'Rice with Sambar'
            ],
            'Before Bed': [
                '1 scoop whey protein with milk',
                '1 small bowl of Greek yogurt'
            ]
        }

    def get_weight_loss_plan(self, day):
        # Adjust quantities based on daily caloric needs
        return {
            'Breakfast (Pre-Workout)': [
                f'{self.adjust_meal_amount(2)} slices whole wheat toast',
                '1 boiled egg or scrambled egg whites',
                f'{self.adjust_meal_amount(1/2)} cup oatmeal with water',
                '1 small apple'
            ],
            'Mid-Morning (Snack)': [
                '1 scoop whey protein with water',
                f'{self.adjust_meal_amount(6)} almonds',
                'Carrot sticks'
            ],
            'Lunch (Low-Calorie)': [
                f'{self.adjust_meal_amount(150)}g grilled chicken breast or fish',
                '150g steamed vegetables',
                f'{self.adjust_meal_amount(100)}g quinoa'
            ],
            'Afternoon Snack': [
                'Herbal tea or black coffee',
                '1 small handful of mixed nuts',
                '1 piece of fruit'
            ],
            'Dinner': [
                f'{self.adjust_meal_amount(150)}g fish or grilled chicken breast',
                'Mixed green salad',
                f'{self.adjust_meal_amount(1/2)} cup cooked lentils'
            ],
            'Before Bed': [
                '1 small bowl of Greek yogurt'
            ]
        }

    def adjust_meal_amount(self, amount):
        # Adjust meal quantities based on daily caloric needs
        base_calories = 2000  # Assumes a base diet for 2000 kcal
        return round(amount * self.daily_calories / base_calories, 1)

# Diet Plan Route
@app.route("/diet", methods=["GET", "POST"])
def diet_plan():
    diet_plan = None
    if request.method == "POST":
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        duration = request.form["duration"]
        diet_type = request.form["diet_type"]
        gender = request.form["gender"]
        activity_level = request.form["activity_level"]

        user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level)
        diet_plan = user.plan

    return render_template("diet.html", diet_plan=diet_plan)






routines = {
    'beginner': {
        'strength': [
            {'exercise': 'Bodyweight Squats', 'sets': 3, 'reps': 10},
            {'exercise': 'Push-ups', 'sets': 3, 'reps': 8},
            {'exercise': 'Plank', 'sets': 3, 'duration': '30 seconds'}
        ],
        'cardio': [
            {'exercise': 'Brisk Walking', 'duration': '20 minutes'},
            {'exercise': 'Jump Rope', 'duration': '5 minutes'},
        ],
        'flexibility': [
            {'exercise': 'Hamstring Stretch', 'duration': '30 seconds'},
            {'exercise': 'Quad Stretch', 'duration': '30 seconds'},
        ]
    },
    'intermediate': {
        'strength': [
            {'exercise': 'Dumbbell Bench Press', 'sets': 4, 'reps': 10},
            {'exercise': 'Dumbbell Rows', 'sets': 4, 'reps': 10},
            {'exercise': 'Lunges', 'sets': 4, 'reps': 10}
        ],
        'cardio': [
            {'exercise': 'Jogging', 'duration': '30 minutes'},
            {'exercise': 'HIIT Circuit', 'duration': '20 minutes'},
        ],
        'flexibility': [
            {'exercise': 'Forward Bend', 'duration': '30 seconds'},
            {'exercise': 'Shoulder Stretch', 'duration': '30 seconds'},
        ]
    },
    'advanced': {
        'strength': [
            {'exercise': 'Barbell Squats', 'sets': 5, 'reps': 8},
            {'exercise': 'Deadlifts', 'sets': 5, 'reps': 8},
            {'exercise': 'Pull-ups', 'sets': 4, 'reps': 6}
        ],
        'cardio': [
            {'exercise': 'Interval Sprints', 'duration': '30 minutes'},
            {'exercise': 'Cycling', 'duration': '45 minutes'},
        ],
        'flexibility': [
            {'exercise': 'Pigeon Pose', 'duration': '30 seconds'},
            {'exercise': 'Cobra Stretch', 'duration': '30 seconds'},
        ]
    }
}

@app.route('/sport', methods=['GET', 'POST'])
def home():
    routine = None
    if request.method == 'POST':
        fitness_level = request.form.get('fitness_level')
        if fitness_level in routines:
            routine = routines[fitness_level]
    return render_template('sports.html', routine=routine)



@app.route("/workout")
def work():
    return render_template("Sections.html")


@app.route("/GP")
def gp():
    return render_template("page5.html")
@app.route("/D1")
def d1():
    return render_template("day1.html")

@app.route("/D3")
def d3():
    return render_template("day3.html")
@app.route("/D4")
def d4():
    return render_template("day4.html")



@app.route("/D2")
def d2():
    return render_template("day2.html")

if __name__ == '__main__':
    app.run(debug=True)

