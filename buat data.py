import csv
import random
import time
from typing import List, Dict, Set, Union, Any
from dataclasses import dataclass
from enum import Enum
import re
import operator

class JobType(Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    FREELANCE = "Freelance"
    REMOTE = "Remote"
    CONTRACT = "Contract"

@dataclass
class Job:
    """Representasi data lowongan kerja"""
    id: int
    position: str
    location: str
    skills: Set[str]
    experience: int
    salary: int
    job_type: JobType
    company: str
    
    def __post_init__(self):
        # Konversi skills ke set jika masih berupa string
        if isinstance(self.skills, str):
            self.skills = set(skill.strip().lower() for skill in self.skills.split(','))
        elif isinstance(self.skills, list):
            self.skills = set(skill.strip().lower() for skill in self.skills)
        else:
            self.skills = set(str(skill).strip().lower() for skill in self.skills)

class JobFilterSystem:
    """Sistem penyaringan lowongan kerja berbasis teori himpunan dan logika Boolean"""
    
    def __init__(self):
        self.jobs: List[Job] = []
        self.skill_universe: Set[str] = set()
        self.location_universe: Set[str] = set()
        self.position_universe: Set[str] = set()
        
    def generate_sample_data(self, filename: str = "job_data.csv", num_jobs: int = 100):
        """Generate data simulasi lowongan kerja yang realistis"""
        
        # Data referensi untuk simulasi
        positions = [
            "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
            "DevOps Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Business Analyst", "Marketing Manager", "Sales Executive", "HR Manager",
            "Quality Assurance", "Project Manager", "Database Administrator", "System Administrator",
            "Machine Learning Engineer", "Cybersecurity Analyst", "Mobile Developer", "Cloud Architect"
        ]
        
        locations = [
            "Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Makassar", "Palembang",
            "Yogyakarta", "Denpasar", "Balikpapan", "Malang", "Tangerang", "Bekasi", "Depok"
        ]
        
        skills_pool = [
            "python", "java", "javascript", "react", "angular", "vue", "node.js", "php",
            "sql", "mysql", "postgresql", "mongodb", "redis", "docker", "kubernetes",
            "aws", "azure", "gcp", "git", "jenkins", "ci/cd", "agile", "scrum",
            "machine learning", "deep learning", "data analysis", "excel", "powerbi",
            "tableau", "figma", "sketch", "photoshop", "html", "css", "bootstrap",
            "tensorflow", "pytorch", "pandas", "numpy", "scipy", "r", "scala",
            "go", "rust", "c++", "c#", ".net", "spring", "django", "flask",
            "project management", "leadership", "communication", "problem solving"
        ]
        
        companies = [
            "TechCorp", "InnovateSoft", "DataTech", "CloudSolutions", "DigitalFirst",
            "StartupX", "MegaCorp", "SmartSystems", "FutureTech", "CodeFactory",
            "DataDriven", "AILabs", "WebMasters", "AppDev", "CyberSecure"
        ]
        
        # Generate data simulasi
        jobs_data = []
        for i in range(num_jobs):
            position = random.choice(positions)
            location = random.choice(locations)
            
            # Generate skills berdasarkan posisi
            num_skills = random.randint(3, 8)
            job_skills = random.sample(skills_pool, num_skills)
            
            # Adjust skills berdasarkan posisi
            if "Developer" in position or "Engineer" in position:
                job_skills.extend(random.sample(
                    ["python", "java", "javascript", "sql", "git"], 
                    random.randint(1, 3)
                ))
            elif "Data" in position:
                job_skills.extend(random.sample(
                    ["python", "sql", "machine learning", "pandas", "numpy"], 
                    random.randint(1, 3)
                ))
            elif "Manager" in position:
                job_skills.extend(random.sample(
                    ["leadership", "project management", "communication"], 
                    random.randint(1, 2)
                ))
            
            job_skills = list(set(job_skills))  # Remove duplicates
            
            job_data = {
                'id': i + 1,
                'position': position,
                'location': location,
                'skills': ','.join(job_skills),
                'experience': random.randint(0, 10),
                'salary': random.randint(5000000, 25000000),
                'job_type': random.choice(list(JobType)).value,
                'company': random.choice(companies)
            }
            jobs_data.append(job_data)
        
        # Tulis ke file CSV
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'position', 'location', 'skills', 'experience', 'salary', 'job_type', 'company']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs_data)
        
        print(f"Data simulasi {num_jobs} lowongan kerja berhasil dibuat di {filename}")
        
    def load_jobs_from_csv(self, filename: str):
        """Load data lowongan kerja dari file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.jobs = []
                
                for row in reader:
                    job = Job(
                        id=int(row['id']),
                        position=row['position'],
                        location=row['location'],
                        skills=row['skills'],
                        experience=int(row['experience']),
                        salary=int(row['salary']),
                        job_type=JobType(row['job_type']),
                        company=row['company']
                    )
                    self.jobs.append(job)
                    
                    # Build universe sets
                    self.skill_universe.update(job.skills)
                    self.location_universe.add(job.location.lower())
                    self.position_universe.add(job.position.lower())
                    
            print(f"Berhasil memuat {len(self.jobs)} lowongan kerja dari {filename}")
            
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan. Membuat data simulasi...")
            self.generate_sample_data(filename)
            self.load_jobs_from_csv(filename)
        except Exception as e:
            print(f"Error saat memuat data: {e}")
    
    def get_jobs_by_criteria(self, criteria: str, value: Union[str, int, Set[str]]) -> Set[int]:
        """Mendapatkan set job IDs berdasarkan kriteria tertentu"""
        matching_jobs = set()
        
        if criteria == "skill":
            if isinstance(value, str):
                value = value.lower()
                for job in self.jobs:
                    if value in job.skills:
                        matching_jobs.add(job.id)
            elif isinstance(value, set):
                for job in self.jobs:
                    if value.intersection(job.skills):
                        matching_jobs.add(job.id)
                        
        elif criteria == "location":
            value = str(value).lower()
            for job in self.jobs:
                if value in job.location.lower():
                    matching_jobs.add(job.id)
                    
        elif criteria == "position":
            value = str(value).lower()
            for job in self.jobs:
                if value in job.position.lower():
                    matching_jobs.add(job.id)
                    
        elif criteria == "experience":
            if isinstance(value, tuple):  # Range (min, max)
                min_exp, max_exp = value
                for job in self.jobs:
                    if min_exp <= job.experience <= max_exp:
                        matching_jobs.add(job.id)
            else:  # Exact match
                for job in self.jobs:
                    if job.experience == value:
                        matching_jobs.add(job.id)
                        
        elif criteria == "salary":
            if isinstance(value, tuple):  # Range (min, max)
                min_sal, max_sal = value
                for job in self.jobs:
                    if min_sal <= job.salary <= max_sal:
                        matching_jobs.add(job.id)
            else:  # Minimum salary
                for job in self.jobs:
                    if job.salary >= value:
                        matching_jobs.add(job.id)
                        
        elif criteria == "job_type":
            if isinstance(value, str):
                for job in self.jobs:
                    if job.job_type.value.lower() == value.lower():
                        matching_jobs.add(job.id)
                        
        return matching_jobs
    
    def parse_boolean_expression(self, expression: str) -> Set[int]:
        """Parse dan evaluasi ekspresi Boolean"""
        # Preprocessing: ganti operator dengan simbol Python
        expression = expression.replace(" AND ", " & ")
        expression = expression.replace(" OR ", " | ")
        expression = expression.replace(" NOT ", " ~ ")
        
        # Extract criteria dari expression
        criteria_pattern = r'(\w+)\s*([<>=!]+)\s*([^&|~()]+)'
        criteria_matches = re.findall(criteria_pattern, expression)
        
        # Build dictionary untuk evaluasi
        eval_dict = {}
        all_job_ids = set(job.id for job in self.jobs)
        
        for criteria, operator_str, value in criteria_matches:
            value = value.strip().strip('"').strip("'")
            
            if criteria == "skill":
                if "," in value:
                    skills = set(skill.strip().lower() for skill in value.split(","))
                    job_set = self.get_jobs_by_criteria("skill", skills)
                else:
                    job_set = self.get_jobs_by_criteria("skill", value)
                    
            elif criteria == "location":
                job_set = self.get_jobs_by_criteria("location", value)
                
            elif criteria == "position":
                job_set = self.get_jobs_by_criteria("position", value)
                
            elif criteria == "experience":
                if ".." in value:  # Range
                    min_val, max_val = map(int, value.split(".."))
                    job_set = self.get_jobs_by_criteria("experience", (min_val, max_val))
                else:
                    if operator_str == ">=":
                        job_set = self.get_jobs_by_criteria("experience", (int(value), 100))
                    elif operator_str == "<=":
                        job_set = self.get_jobs_by_criteria("experience", (0, int(value)))
                    elif operator_str == "=":
                        job_set = self.get_jobs_by_criteria("experience", int(value))
                        
            elif criteria == "salary":
                if ".." in value:  # Range
                    min_val, max_val = map(int, value.split(".."))
                    job_set = self.get_jobs_by_criteria("salary", (min_val, max_val))
                else:
                    job_set = self.get_jobs_by_criteria("salary", int(value))
                    
            elif criteria == "job_type":
                job_set = self.get_jobs_by_criteria("job_type", value)
            
            # Buat identifier unik untuk setiap criteria
            criteria_id = f"{criteria}_{operator_str}_{value}".replace(" ", "_").replace(",", "_")
            eval_dict[criteria_id] = job_set
            
            # Replace dalam expression
            original_pattern = f"{criteria}\\s*{re.escape(operator_str)}\\s*{re.escape(value)}"
            expression = re.sub(original_pattern, criteria_id, expression)
        
        # Evaluasi expression
        try:
            # Implementasi evaluasi manual untuk keamanan
            result = self.evaluate_set_expression(expression, eval_dict, all_job_ids)
            return result
        except Exception as e:
            print(f"Error dalam evaluasi ekspresi: {e}")
            return set()
    
    def evaluate_set_expression(self, expression: str, eval_dict: Dict[str, Set[int]], all_jobs: Set[int]) -> Set[int]:
        """Evaluasi ekspresi himpunan secara manual"""
        # Tokenize expression
        tokens = re.findall(r'[&|~()]|\w+', expression)
        
        # Simple recursive descent parser
        def parse_expression(tokens, pos):
            return parse_or(tokens, pos)
        
        def parse_or(tokens, pos):
            left, pos = parse_and(tokens, pos)
            
            while pos < len(tokens) and tokens[pos] == '|':
                pos += 1  # Skip '|'
                right, pos = parse_and(tokens, pos)
                left = left.union(right)
            
            return left, pos
        
        def parse_and(tokens, pos):
            left, pos = parse_not(tokens, pos)
            
            while pos < len(tokens) and tokens[pos] == '&':
                pos += 1  # Skip '&'
                right, pos = parse_not(tokens, pos)
                left = left.intersection(right)
            
            return left, pos
        
        def parse_not(tokens, pos):
            if pos < len(tokens) and tokens[pos] == '~':
                pos += 1  # Skip '~'
                operand, pos = parse_primary(tokens, pos)
                return all_jobs - operand, pos
            else:
                return parse_primary(tokens, pos)
        
        def parse_primary(tokens, pos):
            if pos < len(tokens) and tokens[pos] == '(':
                pos += 1  # Skip '('
                result, pos = parse_expression(tokens, pos)
                pos += 1  # Skip ')'
                return result, pos
            elif pos < len(tokens) and tokens[pos] in eval_dict:
                return eval_dict[tokens[pos]], pos + 1
            else:
                return set(), pos
        
        try:
            result, _ = parse_expression(tokens, 0)
            return result
        except:
            return set()
    
    def filter_jobs(self, boolean_expression: str) -> Dict[str, Any]:
        """Filter lowongan kerja berdasarkan ekspresi Boolean"""
        start_time = time.time()
        
        # Parse dan evaluasi ekspresi
        matching_job_ids = self.parse_boolean_expression(boolean_expression)
        
        # Ambil job objects yang cocok
        matching_jobs = [job for job in self.jobs if job.id in matching_job_ids]
        
        # Hitung statistik
        total_jobs = len(self.jobs)
        matched_jobs = len(matching_jobs)
        relevance_percentage = (matched_jobs / total_jobs) * 100 if total_jobs > 0 else 0
        processing_time = time.time() - start_time
        
        return {
            'matching_jobs': matching_jobs,
            'total_jobs': total_jobs,
            'matched_count': matched_jobs,
            'relevance_percentage': relevance_percentage,
            'processing_time': processing_time,
            'expression': boolean_expression
        }
    
    def display_results(self, results: Dict[str, Any]):
        """Tampilkan hasil filtering"""
        print(f"\n{'='*80}")
        print(f"HASIL PENYARINGAN LOWONGAN KERJA")
        print(f"{'='*80}")
        print(f"Ekspresi Boolean: {results['expression']}")
        print(f"Total lowongan: {results['total_jobs']}")
        print(f"Lowongan yang cocok: {results['matched_count']}")
        print(f"Persentase relevansi: {results['relevance_percentage']:.2f}%")
        print(f"Waktu pemrosesan: {results['processing_time']:.4f} detik")
        print(f"{'='*80}")
        
        if results['matching_jobs']:
            print(f"\nDETAIL LOWONGAN YANG COCOK:")
            print(f"{'-'*80}")
            
            for i, job in enumerate(results['matching_jobs'][:10], 1):  # Tampilkan maksimal 10
                print(f"\n{i}. {job.position} - {job.company}")
                print(f"   Lokasi: {job.location}")
                print(f"   Tipe: {job.job_type.value}")
                print(f"   Pengalaman: {job.experience} tahun")
                print(f"   Gaji: Rp {job.salary:,}")
                print(f"   Skills: {', '.join(sorted(job.skills))}")
            
            if len(results['matching_jobs']) > 10:
                print(f"\n... dan {len(results['matching_jobs']) - 10} lowongan lainnya")
        else:
            print("\nTidak ada lowongan yang cocok dengan kriteria yang diberikan.")
    
    def get_available_filters(self):
        """Tampilkan filter yang tersedia"""
        print("\n" + "="*60)
        print("FILTER YANG TERSEDIA")
        print("="*60)
        
        print("\n1. SKILLS:")
        skills_sample = sorted(list(self.skill_universe))[:15]
        print(f"   Contoh: {', '.join(skills_sample)}")
        print(f"   Total: {len(self.skill_universe)} skills")
        
        print("\n2. LOKASI:")
        locations = sorted(list(self.location_universe))
        print(f"   Tersedia: {', '.join(locations)}")
        
        print("\n3. POSISI:")
        positions = sorted(list(self.position_universe))
        print(f"   Tersedia: {', '.join(positions)}")
        
        print("\n4. PENGALAMAN:")
        experiences = sorted(set(job.experience for job in self.jobs))
        print(f"   Range: {min(experiences)} - {max(experiences)} tahun")
        
        print("\n5. GAJI:")
        salaries = [job.salary for job in self.jobs]
        print(f"   Range: Rp {min(salaries):,} - Rp {max(salaries):,}")
        
        print("\n6. TIPE PEKERJAAN:")
        job_types = set(job.job_type.value for job in self.jobs)
        print(f"   Tersedia: {', '.join(sorted(job_types))}")
        
        print("\n" + "="*60)
        print("CONTOH EKSPRESI BOOLEAN:")
        print("="*60)
        print("1. skill = 'python' AND location = 'Jakarta'")
        print("2. position = 'engineer' OR position = 'developer'")
        print("3. experience >= 3 AND salary >= 10000000")
        print("4. skill = 'python,java' AND NOT location = 'Jakarta'")
        print("5. job_type = 'Remote' AND experience <= 5")
        print("6. (skill = 'python' OR skill = 'java') AND location = 'Bandung'")

def main():
    """Fungsi utama untuk demonstrasi sistem"""
    print("SISTEM PENYARINGAN LOWONGAN KERJA")
    print("Berbasis Teori Himpunan & Logika Boolean")
    print("="*50)
    
    # Inisialisasi sistem
    system = JobFilterSystem()
    
    # Load data
    system.load_jobs_from_csv("job_data.csv")
    
    # Tampilkan filter yang tersedia
    system.get_available_filters()
    
    # Contoh penggunaan dengan berbagai ekspresi
    test_expressions = [
        "skill = 'python' AND location = 'Jakarta'",
        "position = 'engineer' OR position = 'developer'",
        "experience >= 3 AND salary >= 10000000",
        "skill = 'python,java' AND NOT location = 'Jakarta'",
        "job_type = 'Remote' AND experience <= 5",
        "(skill = 'python' OR skill = 'data') AND location = 'Bandung'"
    ]
    
    print(f"\n{'='*80}")
    print("DEMONSTRASI SISTEM DENGAN BERBAGAI EKSPRESI")
    print(f"{'='*80}")
    
    for i, expression in enumerate(test_expressions, 1):
        print(f"\n{'-'*50}")
        print(f"Test {i}: {expression}")
        print(f"{'-'*50}")
        
        results = system.filter_jobs(expression)
        system.display_results(results)
        
        # Pause untuk readability
        input("\nTekan Enter untuk melanjutkan...")
    
    # Mode interaktif
    print(f"\n{'='*80}")
    print("MODE INTERAKTIF")
    print(f"{'='*80}")
    
    while True:
        print("\nMasukkan ekspresi Boolean (atau 'quit' untuk keluar):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            print("Terima kasih telah menggunakan sistem penyaringan lowongan kerja!")
            break
        
        if user_input:
            try:
                results = system.filter_jobs(user_input)
                system.display_results(results)
            except Exception as e:
                print(f"Error: {e}")
                print("Silakan coba lagi dengan ekspresi yang valid.")

if __name__ == "__main__":
    main()