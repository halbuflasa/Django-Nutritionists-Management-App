# Django Nutritionists Management System Project

## Project Description
This project is a health management system designed for nutritionists to efficiently manage client health data, dietary plans, and meal deliveries. It includes role-based authorization where admins can manage user accounts, and nutritionists can manage patient profiles, menus, and deliveries. The system integrates a main menu template for easy meal planning, reducing repetitive work for large numbers of clients, and features delivery management tools. The project will be built with Django and PostgreSQL.

## User Stories
- **Admin Management**:
  - As an admin, I can register new users and manage existing nutritionists.
- **Nutritionist Features**:
  - As a nutritionist, I can create, view, update, and delete patient profiles.
  - As a nutritionist, I can create a main menu template that includes all meal options for each day.
  - As a nutritionist, I can auto-generate patient meal plans from the main menu template and customize them as needed.
  - As a nutritionist, I can manage deliveries by creating delivery tables, assigning drivers, and providing a driver view.

## Entity Relationship Diagram (ERD)
1. **Users**:
   - Fields: `id`, `username`, `password`, `role`, `email`, `created_at`, `updated_at`
   - Relationships: Users have roles (`Admin`, `Nutritionist`).

2. **Main Menu**:
   - Fields: `id`, `name`, `description`, `created_at`, `updated_at`
   - Relationships: A main menu can include multiple **Meals**.

3. **Patients**:
   - Fields: `id`, `name`, `age`, `weight`, `height`, `health_data`, `nutritionist_id`, `created_at`, `updated_at`
   - Relationships: Assigned to one Nutritionist.

4. **Meals**:
   - Fields: `id`, `name`, `description`, `ingredients`, `portion_size`, `diet_type`, `calories`, `protein`, `fat`, `carbs`, `image`, `main_menu_id`, `created_at`, `updated_at`
   - Relationships: Meals can be associated with **Main Menu** and **Patient Meal Plans**.

5. **Meal Plans**:
   - Fields: `id`, `patient_id`, `date`, `meals`, `created_at`, `updated_at`
   - Relationships: Linked to **Patients**.

6. **Deliveries**:
   - Fields: `id`, `patient_id`, `area`, `location`, `driver_id`, `delivery_time`, `created_at`, `updated_at`
   - Relationships: Linked to **Patients** and assigned **Drivers**.

## Pseudo-Code Implementation (in English)
### 1. User Authentication and Authorization
- Admin users can sign up new nutritionists and manage accounts.
- Users sign in and, if it is their first login, are prompted to change their password.

```python
# Admin user registration
def sign_up_admin():
    if user.is_admin:
        register_new_nutritionist()

# User sign-in and first-time password change
def sign_in_user():
    if first_login:
        redirect_to_change_password()
    else:
        redirect_to_dashboard(user_role)
```

### 2. Generate Patient Meal Plan from Main Menu
- Automatically create a meal plan for each new patient by copying the main menu template.
- The plan can later be adjusted as needed by the nutritionist.

```python
# Generate patient meal plan from main menu
def generate_patient_menu(patient_id):
    main_menu = get_main_menu()
    for meal in main_menu.meals:
        patient_meal = copy.deepcopy(meal)
        patient_meal.patient_id = patient_id
        patient_meal.save()
```

### 3. Update Patient Meal Plan
- Allow nutritionists to update the patient's specific meal plan by modifying the assigned meals.

```python
# Update specific patient meal plan
def update_patient_meal(patient_id, meal_id, new_meal_data):
    patient_menu = get_patient_menu(patient_id)
    meal = patient_menu.get_meal(meal_id)
    if meal:
        meal.update(new_meal_data)
        meal.save()
```

### 4. Delivery Assignment
- Create delivery plans, sorted by area, and assign a driver to each plan.
- Allow drivers to view their assigned deliveries.

```python
# Assign deliveries to drivers
def assign_delivery(driver, area):
    delivery_plan = DeliveryPlan.objects.filter(area=area, assigned_driver=None)
    for plan in delivery_plan:
        plan.assigned_driver = driver
        plan.save()
```


# Wireframe

## 1. Admin Dashboard

**Purpose**: To manage registered nutritionists and handle user accounts.

**Components**:

- **Header**: Contains navigation options like Dashboard, Users, and Logout.

- **User Management Section**:
  - A table listing all nutritionists with fields: `Name`, `Email`, `Role`, `Status`.
  - **Action Buttons**: Add, Edit, Delete.
  - **User Form (Popup)**: Form fields for creating or editing user accounts (`Username`, `Password`, `Email`, `Role`).

- **Summary Section**: Visual summary (e.g., cards) showing the number of users registered.

## 2. Nutritionist Dashboard

**Purpose**: To provide nutritionists with tools to manage patient data, meal plans, and deliveries.

**Components**:

- **Header**: Navigation options for Patients, Meal Plans, Deliveries, Profile, and Logout.

- **Patient Management Section**:
  - **Patient List Table**: Fields such as `Name`, `Age`, `Health Data`, `Assigned Nutritionist`.
  - **Action Buttons**: Add Patient, Edit, Delete.
  - **Add/Edit Patient Form**: Input fields like `Name`, `Age`, `Weight`, `Health Metrics`, `Delivery Information`.

- **Calendar-Based Meal Planning**:
  - **Calendar View**: Visual calendar interface showing meals assigned to patients.
  - **Add Meal Plan Button**: Opens a form to add or edit meals for specific days.

- **Main Menu Template**:
  - **Main Menu Creation Form**: Fields to add new meals (`Meal Name`, `Ingredients`, `Portion Size`, `Diet Type`, `Calories`).
  - **Meal List**: Displays a list of meals, linked to the calendar-based plan.

- **Delivery Management Section**:
  - **Delivery List Table**: Fields such as `Patient Name`, `Driver`, `Delivery Date`, `Location`.
  - **Assign Driver Button**: Opens a form to assign a driver to each delivery.
  - **Driver View Button**: Opens a filtered view showing deliveries assigned to a specific driver.

## 3. Patient Profile Page

**Purpose**: To show detailed patient health and meal information.

**Components**:

- **Patient Overview Section**:
  - **Patient Information**: `Name`, `Age`, `Health Metrics`.
  - **Edit Button**: Allows nutritionists to update patient details.

- **Meal Plan Section**:
  - **Meal Plan Overview**: Displays the current meal plan for the patient.
  - **Action Buttons**: Edit, Update Meal Plan, or Remove Meal.

- **Health Data Section**:
  - A table or card view showing `Weight`, `Height`, `BMR`, `Daily Calorie Intake`.

## 4. Driver Dashboard

**Purpose**: To allow drivers to see and manage their delivery assignments.

**Components**:

- **Header**: Options like Dashboard, Profile, Logout.

- **Delivery Assignments Table**:
  - Fields include `Patient Name`, `Location`, `Delivery Date/Time`.
  - **Map Integration**: Button to open Google Maps with directions to each delivery location.
  - **Status Update Button**: Drivers can mark deliveries as complete.

