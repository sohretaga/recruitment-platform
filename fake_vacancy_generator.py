from recruitment_cp import models
from job.models import Vacancy
from user.models import Employer, CustomUser
import random

position_titles = [
    "Software Engineer",
    "Data Scientist",
    "Marketing Manager",
    "Sales Representative",
    "Graphic Designer",
    "Product Manager",
    "Human Resources Specialist",
    "Accountant",
    "Customer Service Representative",
    "Project Manager",
    "Content Writer",
    "Web Developer",
    "Network Administrator",
    "Business Analyst",
    "Quality Assurance Engineer",
    "Operations Manager",
    "Logistics Coordinator",
    "Financial Analyst",
    "Security Analyst",
    "Data Analyst",
    "Digital Marketing Specialist",
    "Software Development Manager",
    "Marketing Director",
    "Sales Manager",
    "UX/UI Designer",
    "Product Owner",
    "Recruiter",
    "Chief Executive Officer (CEO)",
    "Chief Financial Officer (CFO)",
    "Chief Technology Officer (CTO)",
    "Chief Marketing Officer (CMO)",
    "Chief Operating Officer (COO)",
    "Machine Learning Engineer",
    "Full Stack Developer",
    "Front-End Developer",
    "Back-End Developer",
    "DevOps Engineer",
    "Database Administrator",
    "Business Development Manager",
    "Content Marketing Manager",
    "Social Media Manager",
    "SEO Specialist",
    "Public Relations Specialist",
    "Technical Support Specialist",
    "Help Desk Analyst",
    "Network Security Engineer",
    "Systems Engineer",
    "Business Systems Analyst",
    "Software Quality Assurance Tester",
    "Research Scientist",
    "Copywriter",
    "Technical Writer",
    "Supply Chain Manager",
    "Barista",
    "Electrician",
    "Plumber",
    "Carpenter",
    "Registered Nurse",
    "Teacher",
    "Lawyer",
    "Paralegal",
    "Web Content Manager",
    "Graphic Designer",
    "Web Designer",
    "Mobile Developer",
    "Game Developer",
    "Environmental Engineer",
    "Civil Engineer",
    "Mechanical Engineer",
    "Marketing Analyst",
    "Financial Advisor",
    "Customer Success Manager",
    "Business Intelligence Analyst",
    "Data Engineer",
    "Product Designer",
    "User Experience (UX) Researcher",
    "Software Architect",
    "Cloud Architect",
    "Cybersecurity Analyst",
    "Network Engineer",
    "Data Center Technician",
    "Help Desk Specialist",
    "IT Support Specialist",
    "Software Test Engineer",
    "Quality Assurance Analyst",
    "Business Project Manager",
    "Event Planner",
    "Human Resources Manager",
    "Office Manager",
    "Retail Sales Associate",
    "Chef",
    "Bartender",
    "Hairdresser",
    "Massage Therapist",
    "Fitness Instructor",
    "Social Worker",
    "Therapist",
    "Translator",
    "Interpreter",
    "Pilot",
    "Mechanic",
    "Firefighter",
    "Police Officer"
]

definitions = [
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
    "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of de Finibus Bonorum et Malorum (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, Lorem ipsum dolor sit amet.., comes from a line in section 1.10.32.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
    "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?",
    "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.",
    "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.",
]
salary = [100, 250, 500, 950, 1500, 1200, 1800, 2000, 2250, 3000]
salary_min = [345, 460, 500, 650, 700, 800, 1000, 1200, 1350, 1500]
salary_max = [1600, 1750, 1800, 1950, 2000, 2450, 2700, 2850, 3000]
job_titles = models.ParameterJobCatalogue.objects.all()
career_types = models.ParameterCareerType.objects.all()
career_levels = models.ParameterCareerLevel.objects.all()
preferences = models.ParameterWorkPreference.objects.all()
departments = models.ParameterDepartment.objects.all()
locations = models.ParameterLocation.objects.all()
employemnt_types = models.ParameterEmployeeType.objects.all()
ftes = models.ParameterFTE.objects.all()
experiences = models.ParameterWorkExperience.objects.all()
random_step = [1,2,3,4,5]
superuser = CustomUser.objects.get(is_superuser=True)
keywords = []

for key_id in models.ParameterKeyword.objects.all().values_list('id', flat=True):
    keywords.append(str(key_id))

def run(limit):
    for i in range(1, limit+1):
        Vacancy.objects.create(
            no = i,
            language = 'en',
            employer = Employer.objects.get(user=superuser),
            career_type = random.choice(career_types),
            career_level = random.choice(career_levels),
            location = random.choice(locations),
            fte = random.choice(ftes),
            salary = random.choice(salary),
            salary_minimum = random.choice(salary_min),
            salary_maximum = random.choice(salary_max),
            position_title = random.choice(position_titles),
            job_title = random.choice(job_titles),
            employment_type = random.choice(employemnt_types),
            work_experience = random.choice(experiences),
            work_preference = random.choice(preferences),
            department = random.choice(departments),
            definition = random.choice(definitions),
            keywords = random.sample(set(keywords), random.choice(random_step)),
            status=True
        )
        print(f'Created {i} vacancy...')

def update_keywords():
    vacancies = Vacancy.objects.all()
    counnt = 1
    for vacancy in vacancies:
        vacancy.keywords = random.sample(set(keywords), random.choice(random_step))
        vacancy.save()
        print(f'Updated {counnt} vacancy...')
        counnt += 1