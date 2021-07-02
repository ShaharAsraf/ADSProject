from django.contrib.auth.models import User

from ..models import PersonalityTestItem, PersonalityTestAnswer


def get_personality_type(user_id):
    user = User.objects.get(pk=user_id)
    answers = [answer.answer for answer in PersonalityTestAnswer.objects.filter(user=user_id)]
    test_items_info = PersonalityTestItem.objects.all()

    resault_type = get_personality_trait("IE", answers)
    resault_type += get_personality_trait("SN", answers)
    resault_type += get_personality_trait("FT", answers)
    resault_type += get_personality_trait("JP", answers)

    return resault_type


def get_personality_trait(trait_type, aswners):
    items = PersonalityTestItem.objects.all().filter(type=trait_type)
    score = 0
    substraction_count = 0

    for item in items:
        if item.inversion:
            score -= aswners[item.itemID]
            substraction_count += 1
        else:
            score += aswners[item.itemID]

    teshold_score = (len(items) * 6) // 2 - substraction_count * 6

    if score > teshold_score:
        return trait_type[1]
    else:
        return trait_type[0]
