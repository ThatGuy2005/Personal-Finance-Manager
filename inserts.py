import argon2
import server_communication as sc

# Initialize Argon2id hasher with standard parameters
ph = argon2.PasswordHasher(
    time_cost=2,        # Iterations
    memory_cost=19456,  # 19 MiB memory cost (RFC 9106 recommended default)
    parallelism=1,      # Threads
    hash_len=32,
    type=argon2.Type.ID
)

users = [
    ("Alice Henderson", "alice.h@example.com", "P@ssw0rd_Long_2026!"),
    ("Marcus Thorne", "m.thorne@techflow.io", "Secure#Alpha_99_Xyz"),
    ("Elena Rodriguez", "elena.rod@webmail.org", "B0at_R@ce_Winner_22!"),
    ("David Chen", "dchen88@provider.net", "K3yboard_Cat_#9999"),
    ("Sarah Jenkins", "s.jenkins@domain.com", "Sunsh1ne!_M0ntana_#1"),
    ("Oliwier Nowak", "o.nowak@service.pl", "Stark_Industr1es_@7"),
    ("Amara Okafor", "amara.o@global.edu", "P@thway_To_Success_1"),
    ("Jordan Smith", "jsmith_dev@code.com", "C0ffee_Is_Life_2026#"),
    ("Beatriz Silva", "b.silva@brasil.br", "R1o_De_Janeiro_!992"),
    ("Liam Wilson", "liam.wilson@site.uk", "London_Bridge_#2026")
]

values_list = []
for name, email, plain_password in users:
    # Generates a unique salt and Argon2id hash output string automatically
    hashed_password = ph.hash(plain_password)
    values_list.append(f"('{name}', '{email}', '{hashed_password}')")
sql_query = "INSERT INTO [Users] ([NAME], [EMAIL], [PASSWORD_HASH]) VALUES\n" + ",\n".join(values_list) + ";"
sc.execute(sql_query)