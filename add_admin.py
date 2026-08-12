"""IMPORTANT: This file must be deleted after it was run. 
The credentials must be remembered or stored in a safe space.
If another admin must be introduced, then it should be done via promotion."""

import argon2
import server_communication as sc

# Initialize Argon2id hasher with standard parameters
ph = argon2.PasswordHasher(
    time_cost=2,        # Iterations
    memory_cost=19456,  # 19 MiB memory cost
    parallelism=1,      # Threads
    hash_len=32,
    type=argon2.Type.ID
)

admin_password = "SuperSecureAdminPassword123!"
hashed_admin_password = ph.hash(admin_password)

sql_query = """
INSERT INTO [Users] ([NAME], [EMAIL], [PASSWORD_HASH], [ROLE_ID]) 
VALUES ('System Admin', 'admin@app.com', '{hash}', 2);
"""

sc.execute(sql_query.format(hash=hashed_admin_password))