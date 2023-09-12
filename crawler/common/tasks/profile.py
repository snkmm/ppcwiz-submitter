from crawler import session_scope
from crawler.common.enums import AccountType
from crawler.common.models import Profile, User
from crawler.settings import REFRESH_TOKEN
from crawler.util.utils import refresh_access_token, fetch_profiles
from datetime import datetime


async def crawl_profiles(ref_tok):
    auth_data = await refresh_access_token(ref_tok)
    print(auth_data)
    if (auth_data.get('error', None)):
        print("????????????????????????")
        with session_scope() as session:
            #temp = session.query(User.auth).filter(User.auth > 0).all()
            #print(temp)
            countdown = session.query(User.auth).filter_by(refresh_token=ref_tok)[0][0]
            #countdown = countdown - 1
            #auth_temp.update({'auth': countdown})

            if (countdown > 0):
                countdown -= 1
                auth_temp = session.query(User).filter_by(refresh_token=ref_tok)
                auth_temp.update({'auth': countdown})

        exit("countdown")

    profiles = await fetch_profiles(auth_data['access_token'], auth_data['token_type'].capitalize())

    with session_scope() as session:
        count = 0
        sess_profile = session.query(Profile)

        profile_id_temp = []

        for profile in profiles:
            if profile['accountInfo'].get('validPaymentMethod', None):
                #print("!!!!!!!!!!!!!!!!!!")
                #continue

                db_profile = sess_profile.get(profile['profileId'])
                if db_profile is None:
                    #insert

                    #user = session.query(User).filter_by(business_name=profile['accountInfo']['name']).first()
                    #print(user)

                    #if user is None:
                    #    continue

                    #user = session.query(User).first() #.filter_by(default_profile=profile['id'])

                    session.add(Profile(
                        id=profile['profileId'],
                        country_code=profile['countryCode'],
                        currency_code=profile['currencyCode'],
                        daily_budget=profile['dailyBudget'],
                        marketplace_id=profile['accountInfo']['marketplaceStringId'],
                        account_id=profile['accountInfo']['id'],
                        account_type=AccountType(profile['accountInfo']['type']),
                        account_name=profile['accountInfo']['name'],
                        #user_id=user.id
                    ))

                else:
                    #update
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    df_temp = sess_profile.filter_by(id=profile['profileId'])
                    df      = df_temp.first()
                    print(df.daily_budget)
                    print(profile['dailyBudget'])

                    if (profile['dailyBudget'] != df.daily_budget):
                        print("*******************************")
                        print(df.daily_budget)
                        df_temp.update({'daily_budget': profile['dailyBudget'], 'updated_datetime': datetime.now()})

                    if (profile['accountInfo']['name'] != df.account_name):
                        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                        print(df.account_name)
                        df_temp.update({'account_name': profile['accountInfo']['name'], 'updated_datetime': datetime.now()})

                count += 1
                profile_id_temp.append(profile['profileId'])


        #delete
        if (count < sess_profile.filter_by(account_id=profile['accountInfo']['id']).count()):
            print("-----------------------------------")
            sess_filter = session.query(Profile.id).filter_by(account_id=profile['accountInfo']['id'])

            temp = []
            for i in sess_filter:
                temp.append(i[0])

            #profile_id_temp = []
            #for profile in profiles:
            #    if profile['accountInfo'].get('validPaymentMethod', None):
            #        profile_id_temp.append(profile['profileId'])

            list_temp = list(set(temp) - set(profile_id_temp))
            print(list_temp)
            for i in list_temp:
                sess_profile.filter_by(id=i).delete()

        #update user_id
        for profile in profiles:
            user_id = session.query(User.id).filter_by(default_profile=profile['profileId']).first()
            #print("user id:", user_id)
            if (user_id is not None):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                sess_profile.update({'user_id': user_id[0]})

        #no error and restart from origin state
        countdown = session.query(User.auth).filter_by(refresh_token=ref_tok)[0][0]
        if (countdown < 9):
            auth_temp = session.query(User).filter_by(refresh_token=ref_tok)
            auth_temp.update({'auth': 9})
    print("Done!")
