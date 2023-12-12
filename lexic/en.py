from settings import total_tasks
n = total_tasks

lexicon: dict[str:str] = {
     'msg_from_admin': 'Message from administrator:',
     'help': '⚙️ For questions about checking tasks and problems with the bot, write @its_dmitrii'
             '\n\nList of commands:'
             '\n/language - change language'
             '\n/next - get next task'
             '\n/status - see the list of my tasks'
             '\n/cancel - cancel sending file'
             '\n/personal - specify personal data'
             '\n/instruct - view instructions'
             '\n/start - view welcoming message',

     # cancel command
     'cancel': 'Specify the task numbers (two digits) separated by a space for which you want to cancel sending the file. Example message:'
               '\n\n01 02 16',
     'cancel_fail': 'There are no files you can delete',
     'cancel_ok': 'Ok. Your files have been removed from tasks: ',
     'cancel_not_found': 'Tasks with the following numbers have either already been sent for verification, or you did not send them: ',
     'cancel_wrong_form': 'Invalid format. I expect task numbers separated by spaces.',

     'status': '✅ Accepted - {}\n🔁 Need to redo - {}\n⏳ Under review - {}\n💪 Remaining to do - {}',
     'no_ref': 'The link is invalid. Ask the person who brought you to us for a link.',
     'start': 'Hello!\n\n'
              'We collect photos to <b>train a neural network</b> to recognize emotions. '
              f'You have {n} tasks to complete. Each will contain a photo example and a brief description of what needs to be photographed. '
              f'When you complete all {n} tasks, your files will be sent to us <b>for review</b>.\n\n'
              'If any tasks are not completed correctly, we will reject them and ask you to redo them (not all, but only those completed incorrectly). '
              f'When all {n} tasks are successfully accepted, you will receive a notification, and after that you will receive <b>payment</b> within a week.\n'

              f'\n<b>The tasks themselves</b> - you need {n} photos: 3 facial expressions from 5 angles'
              '\n<b>3 expressions:</b>'
              '\n- Neutral (no smile, mouth closed)'
              '\n- Smile (with or without teeth - it doesn’t matter)'
              '\n- Show teeth (both rows of teeth are clearly visible)'
              '\n<b>5 angles:</b>'
              '\n- Front (full face),'
              '\n- Left profile (90 degrees)'
              '\n- Right profile'
              '\n- Left corner (~45 degrees)'
              '\n- Right corner'

              '\n\nYou can click /next to see all available commands'
              '\nBefore continuing, please read our <b>privacy policy</b> and click the ✅ button.',
     'lang_ok': 'Language set to {}\nTo see a list of commands, press /help',
     'pol_agree': 'I have read and agree to the policy',
     'instuct_agree': 'I have read the requirements',
     'ban': 'Your access to tasks is blocked.',
     'vert': 'You need to shoot vertically, not horizontally. Please redo it.',
     'horiz': 'You need to shoot horizontally, not vertically. Please redo it.',
     'big_file': 'Files heavier than 50 Megabytes are not accepted.',
     'small_file': 'The file weight is only {} MB, this is too low quality. Please shoot in high quality.',
     'privacy_missing': 'Click the checkbox to agree to the privacy policy.',
     'instruct1': 'You need a second person to film as we require a distance of about 1m.'
                  'Check out the <b>requirements</b> for uploaded files:\n'
                  '\n<u>1. Clean Camera</u>: Make sure the lens is not dirty.'
                  '\n<u>2. Resolution from 4K</u>: At least 2100x3800 pixels. You need to shoot with the main phone camera, not the selfie camera.'
                  '\n<u>3. Open face:</u> Your face in the photo is completely open, not covered or cropped.'
                  '\n<u>4. Good lighting:</u> No glare, glare on the face or darkening. White or yellow light.'
                  '\n<u>5. Outsiders:</u> There should be no other people in the frame (neither living nor in pictures), not even their hair or hands.'
                  '\n<u>6. Filming:</u> Any filters/effects/masks are prohibited.'
                  '\n<u>7. Prohibited on the head:</u> headphones, masks, dark glasses, headdresses (except religious ones), drawings on the face, strange costumes.'
                  '\n<u>8. Reflections:</u> There should be no mirrors or other objects in the background or near you where you will be reflected.',

     'full_hd': 'You need to send the file <b>uncompressed</b>. If you do not know how, then'
                ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">look at the example</a> (9 sec).',
     'instruct2': 'You can begin - press the /next command and the bot will show you the next task, then take a photo and send it to this chat.',
     'album': 'Send files one at a time, not in groups',
     'receive': 'Received file for task {}.\nPress /next for next task',
    'all_sent': 'Thank you! You have sent all the necessary files. Please wait for your work to be reviewed.\n'
                 'Press the /personal command to indicate your gender and age, if you have not already specified it.',
     'no_more': 'No tasks available',
     'reject': 'We have checked your work. Unfortunately, some of the files did not pass the exam. Check out our '
               'comments and press /next to get the task.'
               '\nNext in each line is the number of the incorrectly completed task and a comment for it:',
     'all_approved': 'Success! Your set has successfully passed the first quality check.\n'
                     'Within 1-2 days we will check your work more carefully. New corrections may need to be made. '
                     'If everything is done correctly, the person from whom you received the invitation will contact you. Your ID: ',

     # pd
     'age': 'Indicate your age - two numbers together',
     'age_bad': 'Invalid format, I expect two digits',
     'gender': 'Indicate your gender. Send one Latin letter: m (male) or f (female)',
     'gender_bad': 'Invalid format, I expect one Latin letter: m or f',
     'race': 'Please enter your race',
     'fio': 'Please enter your full name',
     'fio_bad': 'Invalid format, I expect two or three words',
     'country': 'Write your country of residence',
     # 'fio_bad': 'Invalid format, I expect two or three words',
     'pd_ok': 'Your data has been saved.',

     'tlk_ok': 'Your data has been saved. '
               'Enter the following data in the Toloka task interface (just touch it to copy):'
               '\n\nVerification code: <code>{}</code>'
               '\n\nTelegram-id: <code>{}</code>',
}