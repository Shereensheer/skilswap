import streamlit as st
from app_logic import SkillSwapApp

def main():
    st.set_page_config(page_title="SkillCircle", page_icon="🔁")
    st.title("🌐 SkillCircle - Swap Skills. Grow Together")

    # Initialize the app logic once
    if "app" not in st.session_state:
        st.session_state.app = SkillSwapApp()
    app = st.session_state.app

    # Query param check for Stripe
    query_params = st.query_params
    if query_params.get("success"):
        st.success("✅ Payment Successful! You are now a Premium User.")
        app.upgrade_to_premium()
    elif query_params.get("canceled"):
        st.warning("❌ Payment canceled.")

    # Sidebar navigation
    menu = ["Home", "Register", "Login", "Dashboard", "Add Course", "Upgrade", "Logout"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.subheader("Welcome to SkillCircle!")
        st.markdown("""
        - 🧠 Learn new skills without spending money.
        - 🔁 Exchange your knowledge with others.
        - 💎 Become a premium user to unlock unlimited access.
        """)

    elif choice == "Register":
        st.subheader("Create Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        if st.button("Register"):
            result = app.register(username, password, email)
            if "successful" in result:
                st.success(result)
            else:
                st.error(result)

    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = app.login(username, password)
            if "Welcome" in result:
                st.success(result)
            else:
                st.error(result)

    elif choice == "Dashboard":
        if app.logged_in_user:
            user = app.logged_in_user
            st.subheader(f"👋 Welcome {user.username}")
            st.write("Your Skills:", user.display_skills())

            skill_to_add = st.text_input("Add a new skill")
            if st.button("Add Skill"):
                result = user.add_skill(skill_to_add)
                st.info(result)

            st.markdown("---")
            st.subheader("Courses Available:")
            for course in app.list_courses():
                st.markdown(f"**{course.name}** — {course.description} — 💰 ₹{course.price}")

            st.markdown("---")
            search_skill = st.text_input("Search for users with this skill")
            if st.button("Find Matches"):
                matches = app.find_matches(search_skill)
                if matches:
                    st.success("Users with that skill: " + ", ".join(matches))
                else:
                    st.warning("No matches found.")
        else:
            st.warning("Please login first.")

    elif choice == "Add Course":
        if app.logged_in_user:
            st.subheader("Add New Course")
            course_name = st.text_input("Course Name")
            course_desc = st.text_area("Course Description")
            course_price = st.number_input("Course Price (₹)", min_value=0, step=1)
            if st.button("Add Course"):
                result = app.add_course(course_name, course_desc, course_price)
                if "successfully" in result:
                    st.success(result)
                else:
                    st.error(result)
        else:
            st.warning("Please login first.")

    elif choice == "Upgrade":
        if app.logged_in_user:
            st.subheader("💎 Upgrade to Premium")
            st.write("Get unlimited skill listings and priority matches.")
            if st.button("Proceed to Stripe Payment ₹500"):
                session_url = app.create_stripe_checkout_session()
                if session_url.startswith("http"):
                    st.markdown(f"[Click here to complete payment]({session_url})", unsafe_allow_html=True)
                else:
                    st.error("Stripe Error: " + session_url)
        else:
            st.warning("Please login first.")

    elif choice == "Logout":
        app.logout()
        st.success("Logged out successfully.")

if __name__ == "__main__":
    main()
