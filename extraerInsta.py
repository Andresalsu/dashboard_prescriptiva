from igramscraper.instagram import Instagram

instagram = Instagram()

# authentication supported
instagram = Instagram.with_credentials('alvarezsuarezandresfelipe', 'Adamklissi2504', '/Users/andalval/Downloads/hello_docker_flask/')
instagram.login()

account = instagram.get_account_by_id(3)
# Available fields
#print('Account info:')
#print('Id', account.identifier)
#print('Username', account.username)
#print('Full name', account.full_name)
#print('Biography', account.biography)
#print('Profile pic url', account.get_profile_pic_url_hd())
#print('External Url', account.external_url)
#print('Number of published posts', account.media_count)
#print('Number of followers', account.followed_by_count)
#print('Number of follows', account.follows_count)
#print('Is private', account.is_private)
#print('Is verified', account.is_verified)
# or simply for printing use 
print(account)