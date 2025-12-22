export interface PersonaField {
  id: string;
  label: string;
  type: 'text' | 'number' | 'textarea' | 'select';
  description: string;
  options?: string[];
}

export interface PersonaGroup {
  name: string;
  fields: PersonaField[];
}

export const personaGroups: Record<string, PersonaGroup> = {
  'A': {
    name: 'Personal Identifiers & Representation',
    fields: [
      { id: 'fullName', label: 'Full Real Name', type: 'text', description: 'Enter the persona\'s complete name to humanize them and make them memorable.' },
      { id: 'pronouns', label: 'Pronouns', type: 'text', description: 'Specify pronouns (e.g., she/her, he/him, they/them) for authentic representation.' },
      { id: 'preferredName', label: 'Preferred Name', type: 'text', description: 'Informal name used in casual contexts (e.g., nickname).' },
      { id: 'signatureQuote', label: 'Signature Quote', type: 'textarea', description: 'A memorable quote that captures the persona\'s voice and perspective.' },
      { id: 'imageStyle', label: 'Image Style', type: 'text', options: ['Casual', 'Formal'], description: 'Choose image style: Casual (approachable) or Formal (credible).' },
      { id: 'privacyPreference', label: 'Privacy Preference', type: 'text', options: ['Low', 'Medium', 'High'], description: 'Level of privacy concern.' }
    ]
  },
  'B': {
    name: 'Core Demographics',
    fields: [
      { id: 'age', label: 'Age', type: 'number', description: 'Current age (affects cognitive abilities, digital skills, and life stage).' },
      { id: 'genderIdentity', label: 'Gender Identity', type: 'text', description: 'Self-identified gender (influences communication styles and expectations).' },
      { id: 'ethnicity', label: 'Ethnicity and Cultural Background', type: 'text', description: 'Cultural identity that shapes norms, values, and communication.' },
      { id: 'nationality', label: 'Nationality', type: 'text', description: 'Country of citizenship or primary residence.' },
      { id: 'legalStatus', label: 'Legal Status', type: 'text', description: 'E.g., citizen, permanent resident, migrant, refugee (affects access rights).' },
      { id: 'politicalOrientation', label: 'Political Orientation', type: 'text', options: ['Conservative', 'Liberal', 'Moderate', 'Apolitical', 'Other'], description: 'If relevant: Political orientation.' }
    ]
  },
  'C': {
    name: 'Language & Communication',
    fields: [
      { id: 'primaryLanguages', label: 'Primary Language(s)', type: 'text', description: 'Main language(s) spoken (determines UI language and localization).' },
      { id: 'communicationStyle', label: 'Communication Style', type: 'text', options: ['Brief/Bullets', 'Detailed/Narrative', 'Mixed'], description: 'Preferred format.' },
      { id: 'tonePreference', label: 'Tone Preference', type: 'text', options: ['Friendly', 'Professional', 'Playful', 'Formal'], description: 'Desired interaction tone.' },
      { id: 'languageRegister', label: 'Language Register', type: 'text', options: ['Formal', 'Informal'], description: 'Formal or Informal address preference.' },
      { id: 'secondaryLanguage', label: 'Secondary Working Language', type: 'text', description: 'Non-native language used in professional contexts.' },
      { id: 'channelPreferences', label: 'Media & Channel Preferences', type: 'text', description: 'Preferred communication channels: Email, SMS, Phone, Social Media, etc.' }
    ]
  },
  'D': {
    name: 'Lifestyle, Routines & Time Patterns',
    fields: [
      { id: 'chronotype', label: 'Chronotype', type: 'text', options: ['Morning person', 'Evening person', 'Intermediate'], description: 'Natural rhythm.' },
      { id: 'peakProductivity', label: 'Peak Productivity Time', type: 'text', description: 'Time of day when most effective (e.g., 9-11 AM).' },
      { id: 'sleepSchedule', label: 'Sleep Schedule', type: 'text', description: 'Typical bedtime and wake-up time.' },
      { id: 'energyFluctuations', label: 'Energy Fluctuations', type: 'textarea', description: 'Times of high/low energy throughout the day.' },
      { id: 'preferredMeetingTime', label: 'Preferred Meeting Time', type: 'text', description: 'Best time for interactions or collaboration.' },
      { id: 'primaryHobbies', label: 'Primary Hobbies', type: 'text', description: 'Main activities during free time.' },
      { id: 'secondaryInterests', label: 'Secondary Interests', type: 'text', description: 'Additional activities or interests.' },
      { id: 'mediaConsumption', label: 'Media Consumption', type: 'text', description: 'Preferred content formats: Podcasts, Video, Articles, Social Media, etc.' },
      { id: 'activityPreference', label: 'Activity Preference', type: 'text', options: ['Solo', 'Group', 'Online', 'Offline', 'Mixed'], description: 'Activity style preference.' },
      { id: 'lifestyleOrientation', label: 'Lifestyle Orientation', type: 'text', description: 'Overall tendencies: Tech-savvy, Fitness-focused, Minimalist, etc.' },
      { id: 'hobbyTime', label: 'Time Spent on Hobbies', type: 'text', description: 'Weekly hours dedicated to leisure activities.' }
    ]
  },
  'E': {
    name: 'Education & Academic Profile',
    fields: [
      { id: 'educationLevel', label: 'Education Level', type: 'text', options: ['High School', 'Associate Degree', 'Bachelor\'s', 'Master\'s', 'PhD', 'Other'], description: 'Highest formal education.' },
      { id: 'academicPerformance', label: 'Average Grades/Performance', type: 'text', description: 'Academic performance level at each education stage.' },
      { id: 'fieldOfStudy', label: 'Field of Study', type: 'text', description: 'Primary academic discipline or major (e.g., Computer Science, Business).' }
    ]
  },
  'F': {
    name: 'Employment & Career',
    fields: [
      { id: 'currentJob', label: 'Current Job', type: 'text', description: 'Present occupation or role title.' },
      { id: 'previousJobs', label: 'Jobs Before This One', type: 'textarea', description: 'Previous roles and industries (brief history).' },
      { id: 'roleAuthority', label: 'Workplace Role Authority', type: 'text', options: ['Entry-level', 'Mid-level', 'Manager', 'Senior Manager', 'Executive'], description: 'Position level.' },
      { id: 'workExperience', label: 'Years of Work Experience', type: 'number', description: 'Total years in professional workforce.' },
      { id: 'industrySector', label: 'Industry Sector', type: 'text', description: 'Professional domain: Healthcare, Finance, Tech, Education, etc.' },
      { id: 'incomeLevel', label: 'Income Level', type: 'text', description: 'Annual income range or bracket.' },
      { id: 'employmentStatus', label: 'Employment Status', type: 'text', options: ['Full-time', 'Part-time', 'Freelance', 'Contract', 'Unemployed', 'Retired'], description: 'Current employment type.' },
      { id: 'workSchedule', label: 'Work Schedule', type: 'text', description: 'Typical working hours and days.' }
    ]
  },
  'G': {
    name: 'Household, Family & Domestic Context',
    fields: [
      { id: 'relationshipStatus', label: 'Relationship Status', type: 'text', options: ['Single', 'Partnered', 'Married', 'Divorced', 'Widowed'], description: 'Current relationship status.' },
      { id: 'householdComposition', label: 'Household Composition', type: 'text', description: 'Who lives with the persona (e.g., spouse, roommates, alone).' },
      { id: 'numDependents', label: 'Number of Dependents', type: 'number', description: 'Count of children or others under care.' },
      { id: 'dependentsAge', label: 'Age of Dependents', type: 'text', description: 'Ages of dependent children or family members.' },
      { id: 'housingType', label: 'Housing Type', type: 'text', options: ['Apartment', 'House', 'Shared Housing', 'Other'], description: 'Type of dwelling.' },
      { id: 'homeOwnership', label: 'Home Ownership', type: 'text', options: ['Own', 'Rent', 'Live with Family'], description: 'Ownership status.' },
      { id: 'homeEnvironment', label: 'Home Environment', type: 'textarea', description: 'Description of space, noise level, privacy, connectivity quality.' }
    ]
  },
  'H': {
    name: 'Financial & Consumer Behavior',
    fields: [
      { id: 'financialHabits', label: 'Financial Habits', type: 'text', options: ['Saver', 'Balanced', 'Spender'], description: 'Spending style.' },
      { id: 'longTermGoals', label: 'Long-Term Economic Goals', type: 'textarea', description: 'Financial aspirations: Retirement savings, property purchase, debt reduction, etc.' },
      { id: 'nextPurchase', label: 'Next Intended Purchase', type: 'text', description: 'Upcoming planned purchase or financial decision.' }
    ]
  },
  'I': {
    name: 'Mobility',
    fields: [
      { id: 'primaryTransport', label: 'Primary Mode of Transport', type: 'text', options: ['Car', 'Public Transit', 'Bike', 'Walking', 'Rideshare'], description: 'Main transportation method.' },
      { id: 'mobilityFrequency', label: 'Mobility Frequency', type: 'text', options: ['Daily', 'Weekly', 'Occasionally', 'Rarely'], description: 'How often they travel.' },
      { id: 'mobilityPurpose', label: 'Mobility Purpose', type: 'text', description: 'Reason for travel: Commute, Caregiving, Leisure, Errands.' },
      { id: 'accessibilityConsiderations', label: 'Accessibility Considerations', type: 'text', description: 'Any mobility limitations or accessibility needs.' },
      { id: 'mobilityRange', label: 'Geographic Mobility Range', type: 'text', options: ['Urban', 'Suburban', 'Rural', 'Mixed'], description: 'Area covered.' }
    ]
  },
  'J': {
    name: 'Health & Accessibility',
    fields: [
      { id: 'healthStatus', label: 'Physical Health Status', type: 'text', options: ['Excellent', 'Good', 'Fair', 'Poor'], description: 'General health condition.' },
      { id: 'chronicConditions', label: 'Chronic Conditions', type: 'textarea', description: 'Ongoing health issues affecting daily life (if any).' },
      { id: 'disabilityStatus', label: 'Disability Status', type: 'text', description: 'Any sensory, cognitive, or motor impairments.' },
      { id: 'accessibilityNeeds', label: 'Accessibility Needs', type: 'textarea', description: 'Required assistive technologies or accommodations.' }
    ]
  },
  'K': {
    name: 'Goals & Priorities',
    fields: [
      { id: 'shortTermPriorities', label: 'Short-to-Medium Term Priorities', type: 'textarea', description: 'Current objectives (next 6-18 months).' },
      { id: 'longTermGoalsPriorities', label: 'Long-Term Life Goals', type: 'textarea', description: 'Major aspirations and values (3+ years).' }
    ]
  },
  'L': {
    name: 'Digital Identity, Platform & Trust',
    fields: [
      { id: 'deviceOwnership', label: 'Digital Device Ownership', type: 'text', description: 'Devices owned: Smartphone, Laptop, Tablet, Desktop, Smartwatch, etc.' },
      { id: 'primaryDevice', label: 'Preferred/Primary Device', type: 'text', options: ['Smartphone', 'Laptop', 'Tablet', 'Desktop'], description: 'Most frequently used device.' },
      { id: 'operatingSystem', label: 'Operating System Ecosystem', type: 'text', options: ['iOS', 'Android', 'Windows', 'macOS', 'Linux', 'Mixed'], description: 'Primary platform.' },
      { id: 'digitalLiteracy', label: 'Digital Literacy Level', type: 'text', options: ['Beginner', 'Intermediate', 'Advanced', 'Expert'], description: 'Technical proficiency.' },
      { id: 'securityPractices', label: 'Security & Privacy Practices', type: 'text', options: ['Low', 'Moderate', 'High'], description: 'Awareness level (e.g., uses password managers, 2FA).' },
      { id: 'trustPropensity', label: 'Trust Propensity', type: 'text', options: ['Low', 'Moderate', 'High'], description: 'General tendency to trust digital systems.' },
      { id: 'digitalActivityFrequency', label: 'Frequency of Digital Activities', type: 'text', options: ['Light', 'Moderate', 'Heavy'], description: 'Daily digital engagement level.' },
      { id: 'techAttitude', label: 'Attitude Towards Technology (ATI Score)', type: 'text', options: ['Technophobe', 'Neutral', 'Technophile'], description: 'Technology affinity.' }
    ]
  },
  'M': {
    name: 'Skills',
    fields: [
      { id: 'professionalSkills', label: 'Professional & Technical Skills', type: 'textarea', description: 'Job-related competencies and expertise.' },
      { id: 'softSkills', label: 'Soft Skills', type: 'text', description: 'Communication, problem-solving, collaboration abilities.' },
      { id: 'learningAgility', label: 'Learning Agility', type: 'text', options: ['Slow', 'Moderate', 'Fast'], description: 'Speed of adapting to new tools.' },
      { id: 'skillMotivation', label: 'Skill Development Motivation', type: 'text', options: ['Low', 'Moderate', 'High'], description: 'Interest in continuous learning.' },
      { id: 'certifications', label: 'Certifications or Credentials', type: 'textarea', description: 'Formal qualifications and professional certifications.' }
    ]
  }
};

