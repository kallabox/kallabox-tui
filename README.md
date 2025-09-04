# KALLABOX-TUI 

**_Kallabox-TUI_** (Textual User Interface), is the UI written in **Python** using the **Textual** package, through which API endpoints of **Kallabox-API** can be accessed easily. Multiple user instances can be created with ease, since all the workings are packaged inside docker containers.

Before proceeding, if you hadn't done it already, set up and run docker and the backend containers, using the procedures given [here](https://github.com/kallabox/kallabox-api#requirements). For detailed understanding of the API, [click here](https://github.com/kallabox/kallabox-api#kallabox-101).

## Getting Started

1. Open a new **Command Line Interface (CLI)**.

2. Navigate to the ***kallabox*** directory, by using the following command.
```
cd kallabox
```
3. Clone the GitHub Repository for ***kallabox-tui***, by using the following command.
```
git clone https://github.com/kallabox/kallabox-tui.git
```
4. Navigate to the newly created ***kallabox-tui*** directory, by using the following command.
```
cd kallabox-tui
```
5. Create the **kallabox-tui** docker container, by using the following command.
```
docker compose create
```

You should be able to see an output like this at the end.

![docker-compose create output](https://github.com/kallabox/kallabox-api/assets/102421860/7697d83e-7a22-4d0f-bdf4-4888792c09ff)

6. Running the container in ***user*** mode and ***service admin*** mode. (Read more about different modes [here](https://github.com/kallabox/kallabox-api#kallabox-101))

7. Now run the docker container, by using the following command.
```
docker compose run kallabox-tui bash
```

You can see a new container terminal like this (The characters after root@ may vary).

![New terminal user](https://github.com/kallabox/kallabox-api/assets/102421860/2f5aca84-93d9-4e41-846e-493ee40b99cd)

### User Mode

To run the TUI in **User** mode, type the following command in the new prompt as shown below

```
python3 main.py
```

![User Terminal Command](https://github.com/kallabox/kallabox-api/assets/102421860/7770d188-9dad-45ac-91c6-91d06f9534b8)

You should be able to see an output like this with a login button below if you scroll down.

![docker-compose run user](https://github.com/kallabox/kallabox-api/assets/102421860/c7085e13-1928-4301-9cad-6d081fda0186)


After Logging in, the **UI** for a regular **User** looks like the one given below.

![user user interface](https://github.com/kallabox/kallabox-api/assets/102421860/f033f08b-4d4f-4464-917c-003591734956)

The **UI** for an **Account Administrator** looks like the one given below (with the added **Account** functionality).

![user admin interface](https://github.com/kallabox/kallabox-api/assets/102421860/6c5688e8-313c-4d3a-a55c-a93b7096af87)

### Service Admin Mode

Alternatively you can run the docker container in ***service admin*** mode, by using the following command as shown below.
```
python3 main.py admin
```

![Super Admin Terminal Command](https://github.com/kallabox/kallabox-api/assets/102421860/c23623da-42d5-4253-b656-34f1ce864706)



You should be able to see an output like this.

![docker-compose run admin](https://github.com/kallabox/kallabox-api/assets/102421860/394beb0e-48dc-4a2b-a013-60646cbcd2c7)

8. If you want to run multiple user and service admin instances, then open some new ***Command Line Interfaces***, and navigate to the ***kallabox-tui*** directory, by using the following command.
```
cd kallabox/kallabox-tui
```

9. Repeat the steps from step 7 to use the TUI in either **User** (or) **Service Admin** mode


### Exiting and Stopping Containers

To exit from the container terminal, use the following command.
```
exit
```

![Exiting from container terminal](https://github.com/kallabox/kallabox-api/assets/102421860/43f73f30-b0e6-4671-b808-dbf764f52e15)

To stop and remove the containers, use the following command.
```
docker compose down
```

Your output should look something like this at the end.

![Docker compose down](https://github.com/kallabox/kallabox-api/assets/102421860/efc3ebf7-2e25-4438-8ae3-6a5daaeb2495)

## Usage

### Navigation 

You can navigate the Textual User Interface (TUI) using the key **TAB** to alternate between menus and **ENTER** (or) **RETURN** key to click the buttons. Alternatively, the **MOUSE POINTER** also works.

### 1. Creating an Account

Let me tell you a narrative that hopefully, will make getting up to speed with using the TUI easier. Also, the characters mentioned here are only for illustration and does not represent real people.

Imagine you are about to start a hotel named **The Cornerstone Delicacy**. A typical hotel has two independent working management teams, namely ***Front of House*** and ***Back of House***. Since, you offer accomodation services, let there be a third team named ***Guest Services***.

Run the TUI as **Service Admin**, and then go to, **Accounts** => **Create Account**, then enter the necessary details and click **Create Account** button after scrolling down.

An example flow chart for creating an account is shown below.

![create account](https://github.com/kallabox/kallabox-api/assets/102421860/f7e87229-e542-4e39-9b3a-bc568f6d4d61)

You hire the following people to take care of each division (by default they will be  **Account Administrators**)
- Ashley  => Front Of House
- Matthew => Back Of House
- Eric    => Guest Services

### 2. Login

Now, Ashley wants to login to the Kallabox-stack. She can use the **Login** functionality as described below.

The **Login** functionality is only required for **Users** (User and Account Administrator) and **not** for Service Administrators. To Login, enter the corresponding **Account**, **Username** and **Password** details and click the **Login** button.

An example flow chart for logging in, for an **account administrator** is shown below.

![login account admin](https://github.com/kallabox/kallabox-api/assets/102421860/e57b36d0-16b6-4a7e-a17d-7d080fb5cfdc)

After [Adding Edward](https://github.com/kallabox/kallabox-tui/tree/main#3-adding-an-user-to-account) **(An User)**, his login flow chart is shown as an example.

![login user](https://github.com/kallabox/kallabox-api/assets/102421860/1344b4d7-0d66-45b3-9490-f44ede14713c)

There is no Account functionality for a regular **User**

### 3. Adding an User to Account

Now, Ashley wants to add Edward to her Front Of House team. She can use the **Add User** functionality as described below.

The **Add User** functionality can only be accessed by **Account Administrators**. To add an user, go to **Account** => **Add User**  and then enter the necessary details and click **Add User** after scrolling down.

An example flow chart for adding an user is shown below

![Add User](https://github.com/kallabox/kallabox-api/assets/102421860/5c7b3660-24eb-4919-9659-c4245879688e)

After adding the necessary users by the respective Account Administrators, the following people are your employees.

1. Front of House Team,
- Ashley -> Account Administrator
- Carol -> Account Administrator
- Edward -> User
- George -> User

2. Back Of House Team,
- Matthew -> Account Administrator
- Debra -> Account Administrator
- Kathleen -> User
- Benjamin -> User

3. Guest Services Team,
- Eric -> Account Administrator
- Christine -> Account Administrator
- Gary -> User
- Nicolas -> User


### 4. Adding Income

The **Add Income** functionality can be used by both **Users** and **Account Administrators**. To add income, go to **Income** => **Add Income** and then enter the amount, and click any one of the modes of payment (Cash, UPI or POS)

An example flow chart for adding income is given below.

![Add Income](https://github.com/kallabox/kallabox-api/assets/102421860/3d579563-f3e3-48d0-9c05-876078160386)

### 5. Getting Income

The **Get Income** functionality can be used by both **Users** and **Account Administrators**. To get incomes, go to **Income** => **Get Income**. 

An example flow chart for getting income is given below.

![Get Income](https://github.com/kallabox/kallabox-api/assets/102421860/fca38ccd-7822-4a4d-9517-cfcf38c84533)

Now, Ashley **(Account Administrator)** can see the incomes entered by all members of the Front Of House team (up) whereas George **(User)** can only see his incomes (down).

### 6. Updating Income 

George **(User)**, incorrectly entered an income in the **9th row** as 55 instead of **59**. So, Ashley **(Account Administrator)** decides to correct the entry, by using the **Update Income** functionality.

The **Update Income** functionality can be used by both **Users** and **Account Administrators**. To update income, go to **Income** => **Update Income** and then enter the **Row Number** and **Corrected Amount** and click the **Update** button.

An example flow chart for updating income is given below.

![Updating Income 1](https://github.com/kallabox/kallabox-api/assets/102421860/988c9c3a-3092-44a2-9f77-bf9a25d71521)

![Updating Income 2](https://github.com/kallabox/kallabox-api/assets/102421860/a38cecb1-405f-4422-b5d0-280b311ba3b2)

### 7. Adding Expenditure

The **Add Expenditure** functionality can be used by both **Users** and **Account Administrators**. To add expenditure, go to **Expenditure** => **Add Expenditure**, and then enter the **amount** and **expense type** and click the **Add** button.

An example flow chart for adding expenditure is given below.

![Adding Expenditure](https://github.com/kallabox/kallabox-api/assets/102421860/7ff41153-fc6b-4c6f-9ccd-8a1fff7919be)

### 8. Getting Expenditure

The **Get Expenditure** functionality can be used by both **Users** and **Account Administrators**. To get expenditures, go to **Expenditure** => **Get Expenditure**.

An example flow chart for getting expenditure is given below.

![Get Expenditure](https://github.com/kallabox/kallabox-api/assets/102421860/f1dc2754-3425-4157-bb1b-dc776cbddec6)

Now, the expenditure list on the top is for the Back of House team as viewed by Matthew **(Account Administrator)** and the one on the bottom is for the Guest Services as viewed by Eric **(Account Administrator)**. Note that the expenditures from the different accounts are **isolated**.

### 9. Updating Expenditure

Benjamin **(User)**, incorrectly entered the expenditure in **2nd row** as 100 instead of **150** and the expense type should be **mushrooms**. So, he decides to change the entry using the **Update Expenditure** functionality.

The **Update Expenditure** functionality can be used by both **Users** and **Account Administrators**. To update expenditure, go to **Expenditure** => **Update Expenditure** and then enter the **Row Number**, **Corrected Expenditure** and **Expense Type** and click the **Update** button.

An example flow chart for updating expenditure is given below.

![Updating Expenditure 1](https://github.com/kallabox/kallabox-api/assets/102421860/610aad76-ff25-4080-b2bb-9f45897742cd)

![Updating Expenditure 2](https://github.com/kallabox/kallabox-api/assets/102421860/3b1b792a-0a45-47e8-be6a-b671f874a7b9)

Note the change in **Amount** and **Expense Type ID**.

### 10. Adding Expense Type

The **Add Expense Type** functionality can be used by both **Users** and **Account Administrators**. To add expense type, go to **Expense Types** => **Add Expense Types**, and then enter the **expense type** and click the **Add** button.

An example flow chart for adding expense type is given below.

![Adding Expense Type](https://github.com/kallabox/kallabox-api/assets/102421860/034c779c-1571-4c61-9584-ec402178c6bc)

### 11. Getting Expense Type

The **Get Expense Type** functionality can be used by both **Users** and **Account Administrators**. To get expense types, go to **Expense Types** => **Get Expense Types**. 

An example flow chart is given below.

![Get Expense Types](https://github.com/kallabox/kallabox-api/assets/102421860/fca13da3-c5e5-4957-9fe3-f67fe3053aa0)

### 12. Updating Expense Types

Benjamin **(User)** wants to update his expense type in **3rd row** from POTATOES to TOMATOES. So, he decides to change the entry using the **Update Expense Type** functionality.

The **Update Expense Type** functionality can be used by both **Users** and **Account Administrators**. To update expense type, go to **Expense Type** => **Update Expense Type** and then enter the **Row Number**, and the correct **expense type** and click the **Update** button.

An example flow chart for updating expense type is given below.

![Updating Expense Type 1](https://github.com/kallabox/kallabox-api/assets/102421860/55d645b9-eb01-4d7c-8397-1c5d52078988)

![Updating Expense Type 2](https://github.com/kallabox/kallabox-api/assets/102421860/a293af51-127c-42f5-bb83-c4cb0e78c7ef)

Note the changed expense type.

### 13. Updating User Role

Christine **(Account Administrator)** of the Guest Services team, sees that Eric **(Account Administrator)** has incurred such huge expenses for the team and decides to downgrade his role to **User**. So, she decides to use the **Update User Role** functionality.

The **Update User Role** functionality can only be used by **Account Administrator**. To update a user's role, go to **Account** => **Update User Role** and then enter the respective **User Name** and **Role** and click the **Update** button.

An example flow chart is given below.

![Updating User Role 1](https://github.com/kallabox/kallabox-api/assets/102421860/12ba6e20-6011-4424-94b9-c3c70385398e)

![Updating User Role 2](https://github.com/kallabox/kallabox-api/assets/102421860/be8e6664-8f1f-4d17-a840-dfc883fb8f7f)

### 14. Deleting User

Christine **(Account Administrator)** of the Guest Services team, still desperate to reduce costs incurred by her team, decides to let go of Nicolas **(User)**. So, she decides to use the **Delete User** functionality.

The **Delete User** functionality can only be used by **Account Administrators**. To delete an user, go to **Account** => **Delete User** and then enter the **Name** of the user (the first one gets deleted) and click the **Delete** button. 

An example flow chart is given below.

![Deleting User 1](https://github.com/kallabox/kallabox-api/assets/102421860/bd64c882-42a6-4184-a1e0-5eec32eca8ad)

![Deleting User 2](https://github.com/kallabox/kallabox-api/assets/102421860/44b2f44e-09ca-49cc-9e26-a03ec944f357)

Note that Nicolas is **not** in the Guest Services team.

### 15. Purging an Account

You **(Service Administrator)**, as owner of the hotel, decide to do the inevitable, letting go of the entire Guest Services division in an effort to cut losses. You can use the **Purge Account** functionality to delete an entire account alongwith its users.

The **Purge Account** functionality can only be used by **Service Administrators**. To purge an account, go to **Account** => **Purge Account** and then enter the **Account Name** and click the **Delete** button.

The final output after deleting **Guest Services** is given below.

![Deleting Account](https://github.com/kallabox/kallabox-api/assets/102421860/61caefa1-517c-4ec2-aa2e-db868c4200e0)

## Known Issue

For **Users** and **Account Administrators**, the lifetime of a login is 24 hours. Hence, accessing any of the functionality after 24 hours may throw a **_Could not validate Credentials Error_**. To resolve, **Logout** and then **Login** again.

## Credits 

To [@shibme](https://github.com/shibme), for guiding me through this project.

