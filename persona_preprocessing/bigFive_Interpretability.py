#!/usr/bin/env python3
import json
import sys

def calculate_big_five_scores(answers):
    """
    Calculate Big Five personality trait scores from test answers.
    
    Args:
        answers: List of dictionaries with questionNumber, question, answer, and answerLabel
    
    Returns:
        Dictionary with scores for each trait
    """
    # Create answer lookup dictionary
    ans = {item['questionNumber']: item['answer'] for item in answers}
    
    # Calculate each trait using the formulas from the scoring sheet
    extroversion = (20 + ans[1] - ans[6] + ans[11] - ans[16] + ans[21] - 
                   ans[26] + ans[31] - ans[36] + ans[41] - ans[46])
    
    agreeableness = (14 - ans[2] + ans[7] - ans[12] + ans[17] - ans[22] + 
                    ans[27] - ans[32] + ans[37] + ans[42] + ans[47])
    
    conscientiousness = (14 + ans[3] - ans[8] + ans[13] - ans[18] + ans[23] - 
                        ans[28] + ans[33] - ans[38] + ans[43] + ans[48])
    
    neuroticism = (38 - ans[4] + ans[9] - ans[14] + ans[19] - ans[24] - 
                  ans[29] - ans[34] - ans[39] - ans[44] - ans[49])
    
    openness = (8 + ans[5] - ans[10] + ans[15] - ans[20] + ans[25] - 
               ans[30] + ans[35] + ans[40] + ans[45] + ans[50])
    
    return {
        'Extroversion': extroversion,
        'Agreeableness': agreeableness,
        'Conscientiousness': conscientiousness,
        'Neuroticism': neuroticism,
        'Openness': openness
    }

def get_score_level(score, max_score=40):
    """Categorize score into low, moderate, or high."""
    percentage = (score / max_score) * 100
    
    if percentage < 35:
        return 'very low'
    elif percentage < 45:
        return 'low'
    elif percentage < 55:
        return 'moderate'
    elif percentage < 65:
        return 'high'
    else:
        return 'very high'

def generate_extroversion_description(score):
    """Generate description for Extroversion trait."""
    level = get_score_level(score)
    
    descriptions = {
        'very low': (
            "You show very low extroversion, indicating a strong preference for solitude and introspection. "
            "You likely feel most energized when alone or in very small, intimate settings. Social gatherings "
            "may feel draining, and you probably need significant time to recharge after social interactions. "
            "You tend to be reserved, preferring to listen rather than speak, and you're selective about sharing "
            "your thoughts. You likely enjoy deep, one-on-one conversations over group activities and may find "
            "small talk particularly exhausting. In work settings, you probably excel at independent tasks and "
            "prefer working behind the scenes rather than being in the spotlight."
        ),
        'low': (
            "You demonstrate low extroversion, suggesting you lean toward introversion. You likely prefer smaller "
            "social circles and quieter environments. While you can enjoy social situations, they tend to be energy-draining "
            "rather than energizing. You probably need alone time to recharge and process your thoughts. You're comfortable "
            "with solitude and may prefer written communication over verbal. In social settings, you tend to observe before "
            "participating and prefer meaningful conversations over superficial chitchat. You likely work well independently "
            "and don't seek out being the center of attention."
        ),
        'moderate': (
            "You show moderate extroversion, indicating you have a balanced approach to social interaction. You're "
            "an ambivert—comfortable in both social situations and solitary activities. You can enjoy parties and group "
            "settings but also appreciate quiet time alone. Your energy levels depend on the context and your mood. "
            "You're adaptable, able to be outgoing when needed but also reflective when appropriate. You likely have a "
            "moderate-sized social circle and are selective about social engagements. You can work well both in teams "
            "and independently, adjusting your approach based on the situation."
        ),
        'high': (
            "You display high extroversion, indicating you're energized by social interaction and external stimulation. "
            "You likely enjoy being around people and feel most alive in social settings. You're comfortable starting "
            "conversations, meeting new people, and being part of group activities. You probably have a wide social network "
            "and enjoy parties, gatherings, and collaborative environments. You tend to think out loud and process ideas "
            "through discussion. Extended periods of solitude may feel uncomfortable or boring. In work environments, "
            "you likely thrive in team settings and enjoy roles that involve interaction with others."
        ),
        'very high': (
            "You exhibit very high extroversion, showing a strong orientation toward the external world and social engagement. "
            "You're highly energized by being around people and likely feel restless when alone for too long. You're naturally "
            "outgoing, enthusiastic, and often the life of the party. You probably have an extensive social network and actively "
            "seek out social opportunities. You're comfortable being the center of attention and may even enjoy public speaking "
            "or performing. You likely prefer constant activity and stimulation, finding quiet or solitary environments "
            "understimulating. You excel in roles requiring high social interaction, networking, and team collaboration."
        )
    }
    
    return descriptions[level]

def generate_agreeableness_description(score):
    """Generate description for Agreeableness trait."""
    level = get_score_level(score)
    
    descriptions = {
        'very low': (
            "You show very low agreeableness, indicating a highly independent and competitive mindset. You prioritize "
            "logic and efficiency over social harmony and aren't afraid to challenge others or voice disagreement. "
            "You tend to be skeptical, direct, and unfiltered in your communication, valuing honesty over politeness. "
            "You're unlikely to compromise your positions to please others and may be seen as argumentative or confrontational. "
            "You're comfortable with conflict and may even find it stimulating. You prioritize your own interests and goals, "
            "and you're not easily swayed by emotional appeals. In professional settings, you're willing to make tough decisions "
            "without being overly concerned about popularity."
        ),
        'low': (
            "You demonstrate low agreeableness, suggesting you're more competitive and skeptical than cooperative. "
            "You value directness and honesty, sometimes at the expense of social niceties. You're not afraid to disagree "
            "or challenge others when you believe you're right. You tend to prioritize your own interests and goals, "
            "and you're less concerned with maintaining harmony if it means compromising on important matters. "
            "You may be perceived as tough-minded or blunt. You're comfortable with debate and aren't easily manipulated "
            "by emotional appeals. You respect strength and competence over warmth and may struggle with excessive empathy."
        ),
        'moderate': (
            "You show moderate agreeableness, indicating a balanced approach between cooperation and assertiveness. "
            "You can be compassionate and cooperative when appropriate but also stand firm when necessary. You value both "
            "harmony and honesty, trying to find middle ground in conflicts. You're generally pleasant and considerate "
            "but won't sacrifice your principles just to be liked. You can adapt your approach based on the situation—"
            "being accommodating with some people and more assertive with others. You balance empathy with rationality "
            "and can be both kind and objective depending on what's needed."
        ),
        'high': (
            "You display high agreeableness, indicating you're naturally cooperative, considerate, and empathetic. "
            "You value harmony and tend to avoid conflict when possible. You're generally trusting, helpful, and compassionate "
            "toward others. You find it easy to understand and share others' feelings, and you're motivated to maintain "
            "positive relationships. You're polite, tactful, and willing to compromise to keep the peace. You're likely "
            "well-liked and seen as approachable and kind. You prefer collaboration over competition and are genuinely "
            "concerned with others' welfare. You may sometimes put others' needs before your own."
        ),
        'very high': (
            "You exhibit very high agreeableness, showing exceptional warmth, empathy, and concern for others. "
            "You're deeply motivated by maintaining harmony and helping others. You're trusting, altruistic, and often "
            "put others' needs ahead of your own. You go out of your way to avoid conflict and may struggle to say no "
            "or set boundaries. You're highly sensitive to others' emotions and can be deeply affected by others' distress. "
            "You're seen as exceptionally kind, generous, and supportive. While these qualities make you a wonderful friend "
            "and team member, you may occasionally be taken advantage of or struggle to assert yourself when necessary."
        )
    }
    
    return descriptions[level]

def generate_conscientiousness_description(score):
    """Generate description for Conscientiousness trait."""
    level = get_score_level(score)
    
    descriptions = {
        'very low': (
            "You show very low conscientiousness, indicating a highly spontaneous and flexible approach to life. "
            "You strongly prefer to go with the flow rather than stick to plans or schedules. You may struggle with "
            "organization, often losing track of belongings or forgetting commitments. You're likely to procrastinate "
            "significantly and may find it very difficult to complete tasks, especially ones you don't find immediately "
            "engaging. You prefer improvisation over preparation and may find rules and structure stifling. While this "
            "gives you great adaptability and creative freedom, it can create challenges in meeting deadlines, maintaining "
            "routines, or fulfilling responsibilities consistently."
        ),
        'low': (
            "You demonstrate low conscientiousness, suggesting a preference for spontaneity over structure. "
            "You tend to be more relaxed about deadlines, organization, and planning. You may procrastinate regularly "
            "and prefer to tackle things as they come rather than preparing in advance. You're comfortable with some "
            "level of disorder and may find rigid schedules constraining. You're flexible and adaptable, able to change "
            "plans easily, though this can sometimes mean leaving things unfinished. While you can be disciplined when "
            "necessary, it requires significant effort, and you generally prefer a more casual, go-with-the-flow approach."
        ),
        'moderate': (
            "You show moderate conscientiousness, indicating a balanced approach between structure and flexibility. "
            "You can be organized and disciplined when needed, but you also know when to relax standards and be spontaneous. "
            "You set goals and work toward them but aren't obsessively perfectionistic. You can create and follow plans "
            "but also adjust them when circumstances change. You're reasonably reliable and responsible but don't let "
            "these qualities dominate your life. You balance preparation with adaptability, finding a middle ground "
            "between complete disorder and rigid structure."
        ),
        'high': (
            "You display high conscientiousness, indicating you're organized, disciplined, and goal-oriented. "
            "You're reliable and responsible, following through on commitments and meeting deadlines consistently. "
            "You prefer structure and planning over spontaneity, and you're comfortable with routines and schedules. "
            "You're detail-oriented, thorough in your work, and take pride in doing things well. You're likely well-prepared "
            "for most situations and keep your environment organized. You have strong self-discipline and can persist "
            "through challenges to achieve your goals. You value efficiency, order, and competence."
        ),
        'very high': (
            "You exhibit very high conscientiousness, showing exceptional organization, discipline, and drive. "
            "You're extremely reliable, always meeting commitments and often exceeding expectations. You have rigorous "
            "standards for yourself and likely others. You're highly goal-oriented, creating detailed plans and systematically "
            "working toward objectives. You maintain high levels of organization in all areas of your life and may feel "
            "uncomfortable with disorder or unpredictability. You're thorough, precise, and perfectionistic in your work. "
            "While these qualities make you highly productive and dependable, you may sometimes struggle to relax, be "
            "spontaneous, or tolerate imperfection in yourself or others."
        )
    }
    
    return descriptions[level]

def generate_neuroticism_description(score):
    """Generate description for Neuroticism trait."""
    level = get_score_level(score)
    
    descriptions = {
        'very low': (
            "You show very low neuroticism (very high emotional stability), indicating exceptional emotional resilience. "
            "You're remarkably calm, even-tempered, and unflappable in the face of stress. You rarely experience anxiety, "
            "worry, or mood swings, maintaining composure in challenging situations that might overwhelm others. You're "
            "generally optimistic and don't dwell on negative experiences. You recover quickly from setbacks and don't "
            "take criticism personally. While this stability is a great strength, you may occasionally underestimate risks "
            "or fail to prepare adequately for potential problems because you don't naturally worry about them."
        ),
        'low': (
            "You demonstrate low neuroticism (high emotional stability), suggesting you're generally calm and emotionally "
            "resilient. You handle stress well and don't get overwhelmed easily. You're typically in a stable, positive mood "
            "and don't experience frequent anxiety or worry. You're able to stay composed under pressure and bounce back "
            "from disappointments relatively quickly. You're not easily rattled by criticism or setbacks. While you can "
            "experience negative emotions, they don't dominate your experience or significantly disrupt your functioning."
        ),
        'moderate': (
            "You show moderate neuroticism, indicating a balanced emotional responsiveness. You experience the normal "
            "range of human emotions, including stress, worry, and occasional mood swings, but these don't overwhelm you. "
            "You're appropriately concerned about potential problems without being paralyzed by anxiety. You can handle "
            "most stressful situations adequately, though particularly intense stress may affect you. You have both emotional "
            "sensitivity and resilience, allowing you to respond appropriately to life's challenges without being either "
            "too detached or too reactive."
        ),
        'high': (
            "You display high neuroticism (low emotional stability), indicating you're emotionally sensitive and reactive. "
            "You tend to experience stress, anxiety, and worry more intensely than others. You may find yourself overthinking "
            "situations, anticipating problems, or dwelling on past mistakes. Your moods can fluctuate, and you're more "
            "vulnerable to feeling overwhelmed by life's challenges. You may be self-critical and take criticism from others "
            "quite personally. While this sensitivity can be challenging, it also means you're attuned to potential problems "
            "and may be motivated to address them proactively."
        ),
        'very high': (
            "You exhibit very high neuroticism (very low emotional stability), showing significant emotional reactivity "
            "and vulnerability to stress. You likely experience frequent anxiety, worry, and mood swings. Stressful situations "
            "can feel overwhelming, and you may struggle to manage intense emotions. You probably worry extensively about "
            "potential problems and may ruminate on negative experiences. You're highly sensitive to criticism and may have "
            "difficulty recovering from setbacks. Your emotional intensity affects your daily life significantly. It's important "
            "to develop coping strategies, such as mindfulness, therapy, or stress management techniques, to help navigate "
            "these challenges and improve your emotional wellbeing."
        )
    }
    
    return descriptions[level]

def generate_openness_description(score):
    """Generate description for Openness to Experience trait."""
    level = get_score_level(score)
    
    descriptions = {
        'very low': (
            "You show very low openness to experience, indicating a strong preference for the familiar, concrete, and practical. "
            "You're most comfortable with routines, traditions, and established ways of doing things. You prefer concrete facts "
            "over abstract ideas and may find philosophical or theoretical discussions uninteresting or confusing. You're "
            "skeptical of new or unconventional ideas and prefer proven methods. You likely have conventional tastes and aren't "
            "drawn to artistic or cultural exploration. You value predictability and structure, finding comfort in the known "
            "rather than seeking novelty. While this gives you stability and focus, you may miss out on growth opportunities "
            "that come from new experiences."
        ),
        'low': (
            "You demonstrate low openness to experience, suggesting you prefer the familiar over the novel. You're practical "
            "and down-to-earth, focusing on concrete realities rather than abstract possibilities. You're comfortable with "
            "routines and may be resistant to change or new ways of doing things. You prefer conventional approaches and may "
            "be skeptical of unconventional or innovative ideas. You're not particularly drawn to artistic, philosophical, "
            "or intellectual pursuits. You value stability, tradition, and practical knowledge. While you can adapt when necessary, "
            "you generally prefer what's tried and true."
        ),
        'moderate': (
            "You show moderate openness to experience, indicating a balance between the conventional and the novel. "
            "You can appreciate both familiar routines and new experiences, depending on context. You're open to some new ideas "
            "but also value tradition and proven methods. You can engage with abstract concepts when needed but also appreciate "
            "practical, concrete information. You have varied interests that include both conventional and creative pursuits. "
            "You're adaptable, able to embrace change when it seems beneficial while maintaining some consistency in your life."
        ),
        'high': (
            "You display high openness to experience, indicating intellectual curiosity and appreciation for novelty. "
            "You're drawn to new ideas, experiences, and ways of thinking. You enjoy abstract and theoretical discussions "
            "and can think creatively about complex problems. You likely appreciate art, culture, and intellectual pursuits. "
            "You're imaginative, often thinking beyond conventional boundaries. You embrace change and variety, finding routine "
            "somewhat boring. You're willing to question traditions and explore unconventional perspectives. You're intellectually "
            "engaged with the world and constantly seeking to expand your understanding and experience."
        ),
        'very high': (
            "You exhibit very high openness to experience, showing exceptional intellectual curiosity and love of novelty. "
            "You're deeply engaged with ideas, art, philosophy, and creative expression. You have a vivid imagination and "
            "think abstractly with ease. You're constantly seeking new experiences, knowledge, and perspectives. You may be "
            "unconventional in your thinking and lifestyle, questioning norms and exploring alternative viewpoints. You're "
            "highly creative, appreciating beauty and complexity in various forms. Routine feels stifling to you, and you "
            "need variety and intellectual stimulation. While this makes you innovative and cultured, you may sometimes struggle "
            "with practical matters or find it difficult to relate to more conventional perspectives."
        )
    }
    
    return descriptions[level]

def generate_personality_report(json_data):
    """
    Generate a complete personality report from JSON test data.
    
    Args:
        json_data: Either a JSON string or list of answer dictionaries
                  Each dictionary should contain: questionNumber, question, answer, answerLabel
    
    Returns:
        Dictionary containing scores, levels, and descriptions
    """
    # Parse JSON if string provided
    if isinstance(json_data, str):
        answers = json.loads(json_data)
    else:
        answers = json_data
    
    # Calculate scores
    scores = calculate_big_five_scores(answers)
    
    # Generate report
    report = {
        'scores': scores,
        'levels': {},
        'descriptions': {}
    }
    
    # Add levels and descriptions for each trait
    trait_generators = {
        'Extroversion': generate_extroversion_description,
        'Agreeableness': generate_agreeableness_description,
        'Conscientiousness': generate_conscientiousness_description,
        'Neuroticism': generate_neuroticism_description,
        'Openness': generate_openness_description
    }
    
    for trait, generator_func in trait_generators.items():
        score = scores[trait]
        level = get_score_level(score)
        report['levels'][trait] = level
        report['descriptions'][trait] = generator_func(score)
    
    return report

def print_personality_report(report):
    """Print a formatted personality report."""
    print("="*80)
    print("BIG FIVE PERSONALITY TEST RESULTS")
    print("="*80)
    print()
    
    # Print scores summary
    print("SCORE SUMMARY:")
    print("-" * 80)
    for trait, score in report['scores'].items():
        level = report['levels'][trait]
        print(f"{trait:20s}: {score:2d}/40  ({level.upper()})")
    print()
    
    # Print narrative summary
    print("NARRATIVE SUMMARY:")
    print("-" * 80)
    summary_parts = []
    for trait, score in report['scores'].items():
        level = report['levels'][trait]
        summary_parts.append(f"{level} {trait} {score}/40")
    
    print(f"According to the Big Five Personality Test (BFPT), the individual self-reports "
          f"{', '.join(summary_parts[:-1])}, and {summary_parts[-1]}.")
    print()
    
    # Print detailed descriptions
    print("DETAILED TRAIT DESCRIPTIONS:")
    print("=" * 80)
    
    trait_order = ['Extroversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']
    
    for trait in trait_order:
        print()
        print(f"{trait.upper()} ({report['levels'][trait].upper()} - {report['scores'][trait]}/40)")
        print("-" * 80)
        print(report['descriptions'][trait])
        print()

# Example usage
if __name__ == "__main__":
    # Check if a file argument was provided
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            report = generate_personality_report(data)
            print_personality_report(report)
        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file '{json_file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python3 bigFive_Interpretability.py <json_file>", file=sys.stderr)
        print("Example: python3 bigFive_Interpretability.py answers.json", file=sys.stderr)
        sys.exit(1)