# app_logic.py

import streamlit as st
from user import User
from course import Course
import stripe

import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # ✅


class SkillSwapApp:
    def __init__(self):
        # Initialize or fetch users
        if "users" not in st.session_state:
            st.session_state["users"] = []
        self.users = st.session_state["users"]

        # Initialize or fetch logged-in user
        if "logged_in_user" not in st.session_state:
            st.session_state["logged_in_user"] = None
        self.logged_in_user = st.session_state["logged_in_user"]

        # Initialize or fetch courses
        if "courses" not in st.session_state:
            default_courses = [
                Course("Python Basics", "Learn the basics of Python programming.", 1000),
                Course("Web Development", "Introduction to HTML, CSS, and JavaScript.", 1500),
                Course("Data Science", "Learn data analysis and visualization.", 2000),
            ]
            st.session_state["courses"] = default_courses
        self.courses = st.session_state["courses"]

    def register(self, username, password, email):
        if any(user.username == username for user in self.users):
            return "⚠️ Username already taken."
        new_user = User(username, password, email)
        self.users.append(new_user)
        st.session_state["users"] = self.users
        return "✅ Registration successful."

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                st.session_state["logged_in_user"] = user
                self.logged_in_user = user
                return f"✅ Welcome, {username}!"
        return "❌ Invalid credentials."

    def logout(self):
        st.session_state["logged_in_user"] = None
        self.logged_in_user = None

    def find_matches(self, skill):
        matches = [user.username for user in self.users if skill.lower() in [s.lower() for s in user.skills]]
        return matches

    def add_course(self, name, description, price):
        if not name or not description or price < 0:
            return "⚠️ Invalid course details."
        new_course = Course(name, description, price)
        self.courses.append(new_course)
        st.session_state["courses"] = self.courses
        return f"✅ Course '{name}' added successfully."

    def list_courses(self):
        return self.courses

    def create_stripe_checkout_session(self, price_inr=50000, product_name="SkillCircle Premium Membership"):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "product_data": {"name": product_name},
                            "unit_amount": price_inr,
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url="http://localhost:8501/?success=true",
                cancel_url="http://localhost:8501/?canceled=true",
            )
            return checkout_session.url
        except Exception as e:
            return f"❌ Stripe error: {str(e)}"

    def upgrade_to_premium(self):
        if self.logged_in_user:
            self.logged_in_user.is_premium = True
            return "✨ You are now a premium member!"
        return "⚠️ User not logged in."

