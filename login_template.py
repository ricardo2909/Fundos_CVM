import streamlit as st
import pandas as pd
import FundosCVM

#######################################
# Security LOGIN
import hashlib

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
def create_usertable():
    with open('userstable.txt', 'w') as file:
        file.write('username,password\n')

def add_userdata(username, password):
    with open('userstable.txt', 'a') as file:
        file.write(f'{username},{password}\n')

def login_user(username, password):
    with open('userstable.txt', 'r') as file:
        lines = file.readlines()[1:]  # skip header row
        for line in lines:
            fields = line.strip().split(',')
            if fields[0] == username and fields[1] == password:
                return fields
        return None

def view_all_users():
    with open('userstable.txt', 'r') as file:
        lines = file.readlines()[1:]  # skip header row
        data = [line.strip().split(',') for line in lines]
        return data

######################################





def main():
    import FundosCVM
    """Simple Login App"""

    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))

            if result:
                st.success("Logged In as {}".format(username))

                FundosCVM.app()

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created an Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
