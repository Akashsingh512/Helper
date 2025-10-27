import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP,
                  is_verified INTEGER DEFAULT 0,
                  is_admin INTEGER DEFAULT 0)''')
    
    # Create default admin if not exists
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute('''INSERT OR IGNORE INTO users (username, email, password, is_verified, is_admin)
                 VALUES (?, ?, ?, 1, 1)''', ("admin", "admin@example.com", admin_password))
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        hashed_pw = hash_password(password)
        c.execute('''INSERT INTO users (username, email, password, created_at)
                     VALUES (?, ?, ?, ?)''', 
                  (username, email, hashed_pw, datetime.now()))
        conn.commit()
        conn.close()
        return True, "Registration successful! Wait for admin approval."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute('''SELECT id, username, is_verified, is_admin FROM users 
                 WHERE username=? AND password=?''', (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    
    if user:
        if user[2] == 0:  # is_verified
            return None, "Your account is pending admin approval."
        return user, "Login successful!"
    return None, "Invalid username or password!"

def get_pending_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT id, username, email, created_at FROM users 
                 WHERE is_verified=0''')
    users = c.fetchall()
    conn.close()
    return users

def verify_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET is_verified=1 WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

def show_auth_page():
    init_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        return True
    
    st.title("🔐 Authentication")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Admin Panel"])
    
    # Login Tab
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if login_username and login_password:
                user, message = login_user(login_username, login_password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.session_state.is_admin = user[3]
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please fill in all fields!")
    
    # Register Tab
    with tab2:
        st.subheader("Register")
        reg_username = st.text_input("Username", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register"):
            if reg_username and reg_email and reg_password and reg_confirm:
                if reg_password == reg_confirm:
                    success, message = register_user(reg_username, reg_email, reg_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Passwords don't match!")
            else:
                st.warning("Please fill in all fields!")
    
    # Admin Panel Tab
    with tab3:
        st.subheader("Admin Panel")
        admin_user = st.text_input("Admin Username", key="admin_user")
        admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
        
        if st.button("Admin Login"):
            user, message = login_user(admin_user, admin_pass)
            if user and user[3] == 1:  # is_admin
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid admin credentials!")
        
        if st.session_state.get('admin_logged_in', False):
            st.success("✅ Admin Access Granted")
            st.markdown("---")
            pending_users = get_pending_users()
            
            if pending_users:
                st.subheader("Pending User Approvals")
                for user in pending_users:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    col1.write(f"**{user[1]}** ({user[2]}) - {user[3]}")
                    if col2.button("✅ Approve", key=f"approve_{user[0]}"):
                        verify_user(user[0])
                        st.success(f"Approved {user[1]}")
                        st.rerun()
                    if col3.button("❌ Reject", key=f"reject_{user[0]}"):
                        delete_user(user[0])
                        st.warning(f"Rejected {user[1]}")
                        st.rerun()
            else:
                st.info("No pending approvals")
    
    return False

# Usage: Call this function before your main app
# if show_auth_page():
#     st.write("Welcome to main application!")
#     # Your main app code here