import csv
import time

class JobFilter:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.jobs_data = []
        self.user_preferences = {}
        
    def load_data(self):
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.jobs_data = list(reader)
            print(f"Berhasil memuat {len(self.jobs_data)} data lowongan kerja")
            return True
        except FileNotFoundError:
            print(f"File {self.csv_file} tidak ditemukan!")
            return False
        except Exception as e:
            print(f" Error membaca file: {e}")
            return False
    
    def parse_skills(self, skills_str):
        #Parsing skills dari string ke list
        if not skills_str or skills_str.strip() == '':
            return []
        
        skills_str = skills_str.strip().strip('"')
        skills = [skill.strip().lower() for skill in skills_str.split(',') if skill.strip()]
        return skills
    
    def get_unique_values(self, column):
        #Mendapatkan nilai unik dari kolom tertentu
        unique_values = set()
        for job in self.jobs_data:
            value = job.get(column, '')
            if value:
                if column == 'skills':
                    skills_list = self.parse_skills(value)
                    unique_values.update(skills_list)
                else:
                    unique_values.add(value.strip())
        return sorted(list(unique_values))
    
    def boolean_input(self, question):
        while True:
            response = input(f"{question} (0=Tidak, 1=Ya): ").strip()
            if response in ['0', '1']:
                return int(response)
            print("Masukkan 0 atau 1!")
    
    def get_user_preferences(self):
        print("\n" + "="*50)
        print("PENGATURAN PREFERENSI PENCARIAN")
        print("="*50)
        
        # Preferensi Lokasi
        print("\n1. LOKASI")
        locations = self.get_unique_values('location')
        print(f"Tersedia: {', '.join(locations)}")
        
        use_location = self.boolean_input("Filter berdasarkan lokasi?")
        preferred_locations = []
        
        if use_location:
            for location in locations:
                if self.boolean_input(f"Tertarik dengan '{location}'?"):
                    preferred_locations.append(location)
        
        # Preferensi Skill
        print("\n2. SKILL")
        skills = self.get_unique_values('skills')
        print(f"Tersedia: {', '.join(skills)}")
        
        use_skills = self.boolean_input("Filter berdasarkan skill?")
        preferred_skills = []
        
        if use_skills:
            for skill in skills:
                if self.boolean_input(f"Memiliki skill '{skill}'?"):
                    preferred_skills.append(skill.lower())
        
        # Preferensi Gaji Minimum
        print("\n3. GAJI")
        use_salary = self.boolean_input("Filter berdasarkan gaji minimum?")
        min_salary = 0
        
        if use_salary:
            while True:
                try:
                    min_salary = float(input("Gaji minimum: "))
                    break
                except ValueError:
                    print("Masukkan angka yang valid!")
        
        # Preferensi Jenis Pekerjaan
        print("\n4. JENIS PEKERJAAN")
        job_types = self.get_unique_values('job_type')
        print(f"Tersedia: {', '.join(job_types)}")
        
        use_job_type = self.boolean_input("Filter berdasarkan jenis pekerjaan?")
        preferred_job_types = []
        
        if use_job_type:
            for job_type in job_types:
                if self.boolean_input(f"Tertarik dengan '{job_type}'?"):
                    preferred_job_types.append(job_type)
        
        # Preferensi Pengalaman
        print("\n5. PENGALAMAN")
        use_experience = self.boolean_input("Filter berdasarkan pengalaman?")
        max_experience = float('inf')
        
        if use_experience:
            while True:
                try:
                    max_experience = float(input("Pengalaman maksimum (tahun): "))
                    break
                except ValueError:
                    print("Masukkan angka yang valid!")
        
        # Simpan preferensi
        self.user_preferences = {
            'locations': preferred_locations,
            'skills': preferred_skills,
            'min_salary': min_salary,
            'job_types': preferred_job_types,
            'max_experience': max_experience,
            'use_location': use_location,
            'use_skills': use_skills,
            'use_salary': use_salary,
            'use_job_type': use_job_type,
            'use_experience': use_experience
        }
    
    def match_job(self, job):
        #Mencocokkan job dengan preferensi pengguna
        conditions = []
        
        # Kondisi Lokasi
        if self.user_preferences['use_location'] and self.user_preferences['locations']:
            job_location = job.get('location', '').strip()
            conditions.append(job_location in self.user_preferences['locations'])
        
        # Kondisi Skill
        if self.user_preferences['use_skills'] and self.user_preferences['skills']:
            job_skills = self.parse_skills(job.get('skills', ''))
            user_skills_set = set(self.user_preferences['skills'])
            job_skills_set = set(job_skills)
            conditions.append(bool(user_skills_set & job_skills_set))
        
        # Kondisi Gaji
        if self.user_preferences['use_salary']:
            try:
                job_salary = float(job.get('salary', 0))
                conditions.append(job_salary >= self.user_preferences['min_salary'])
            except (ValueError, TypeError):
                conditions.append(False)
        
        # Kondisi Jenis Pekerjaan
        if self.user_preferences['use_job_type'] and self.user_preferences['job_types']:
            job_type = job.get('job_type', '').strip()
            conditions.append(job_type in self.user_preferences['job_types'])
        
        # Kondisi Pengalaman
        if self.user_preferences['use_experience']:
            try:
                job_experience = float(job.get('experience', 0))
                conditions.append(job_experience <= self.user_preferences['max_experience'])
            except (ValueError, TypeError):
                conditions.append(False)
        
        return all(conditions) if conditions else True
    
    def filter_jobs(self):
        import time
        start_time = time.perf_counter() 
        print("\nMemproses...")
        
        matching_jobs = [job for job in self.jobs_data if self.match_job(job)]
        
        end_time = time.perf_counter()
        processing_time = end_time - start_time
        
        return matching_jobs, processing_time
    
    def display_results(self, matching_jobs, processing_time):
        print("\n" + "="*50)
        print("HASIL PENCARIAN")
        print("="*50)
        
        print(f"Waktu proses: {processing_time:.4f} detik")
        print(f"Lowongan cocok: {len(matching_jobs)} dari {len(self.jobs_data)}")
        
        if matching_jobs:
            print(f"Persentase: {(len(matching_jobs)/len(self.jobs_data)*100):.2f}%\n")
            
            for i, job in enumerate(matching_jobs, 1):
                print(f"{i}. {job.get('position', 'N/A')} - {job.get('company', 'N/A')}")
                print(f"   Lokasi: {job.get('location', 'N/A')}")
                print(f"   Gaji: Rp {float(job.get('salary', 0)):,.0f}")
                print(f"   Pengalaman: {job.get('experience', 'N/A')} tahun")
                print(f"   Jenis: {job.get('job_type', 'N/A')}")
                
                skills_parsed = self.parse_skills(job.get('skills', ''))
                print(f"   Skills: {', '.join(skills_parsed) if skills_parsed else 'N/A'}")
                print(f"   ID: {job.get('id', 'N/A')}\n")
        else:
            print("\n✗ Tidak ada lowongan yang cocok.")

def main():
    print("="*50)
    print("SISTEM FILTERING LOWONGAN KERJA")
    print("="*50)
    
    job_filter = JobFilter('job_data_2.csv')
    
    if not job_filter.load_data():
        return
    
    job_filter.get_user_preferences()
    
    # Filter jobs
    matching_jobs, processing_time = job_filter.filter_jobs()
    
    # Tampilkan hasil
    job_filter.display_results(matching_jobs, processing_time)
    
    print("\nTerima kasih!")

if __name__ == "__main__":
    main()