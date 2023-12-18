from settings import total_tasks
n = total_tasks

lexicon: dict[str:str] = {
      'msg_from_admin': 'Pesan dari administrator:',
      'help': '⚙️ Untuk pertanyaan tentang pemeriksaan tugas dan masalah dengan bot, tulis @its_dmitrii'
              '\n\nDaftar perintah:'
              '\n/language - ganti bahasa'
              '\n/next - dapatkan tugas berikutnya'
              '\n/status - lihat daftar tugas saya'
              '\n/cancel - batalkan pengiriman file'
              '\n/personal - tentukan data pribadi'
              '\n/instruct - lihat instruksi'
              '\n/start - lihat pesan selamat datang',

      # batalkan perintah
      'cancel': 'Tentukan nomor tugas (dua digit) dipisahkan dengan spasi yang ingin Anda batalkan pengiriman filenya. Contoh pesan:'
                '\n\n01 02 16',
      'cancel_fail': 'Tidak ada file yang dapat Anda hapus',
      'batal_ok': 'Oke. File Anda telah dihapus dari tugas: ',
      'cancel_not_found': 'Tugas dengan nomor berikut telah dikirim untuk verifikasi, atau Anda tidak mengirimkannya:',
      'cancel_wrong_form': 'Format tidak valid. Saya berharap nomor tugas dipisahkan dengan spasi.',

      'status': '✅ Diterima - {}\n🔁 Perlu dilakukan ulang - {}\n⏳ Dalam peninjauan - {}\n💪 Masih harus dilakukan - {}',
      'no_ref': 'Tautannya tidak valid. Mintalah tautan kepada orang yang membawa Anda kepada kami.',
      'mulai': 'Halo!\n\n'
               'Kami mengumpulkan foto untuk <b>melatih jaringan saraf</b> untuk mengenali emosi. '
               f'Anda mempunyai {n} tugas yang harus diselesaikan. Masing-masing akan berisi contoh foto dan penjelasan singkat tentang apa yang perlu difoto. '
               f'Saat Anda menyelesaikan semua {n} tugas, file Anda akan dikirimkan kepada kami <b>untuk ditinjau</b>.\n\n'
               'Jika ada tugas yang tidak diselesaikan dengan benar, kami akan menolaknya dan meminta Anda mengulanginya (tidak semua, tetapi hanya tugas yang diselesaikan dengan salah). '
               f'Ketika semua {n} tugas berhasil diterima, Anda akan menerima pemberitahuan, dan setelah itu Anda akan menerima <b>pembayaran</b> dalam waktu seminggu.\n'

               f'\n<b>Tugasnya sendiri</b> - Anda memerlukan {n} foto: 3 ekspresi wajah dari 5 sudut'
               '\n<b>3 ekspresi:</b>'
               '\n- Netral (tidak tersenyum, mulut tertutup)'
               '\n- Tersenyumlah (dengan atau tanpa gigi - tidak masalah)'
               '\n- Tunjukkan gigi (kedua baris gigi terlihat jelas)'
               '\n<b>5 sudut:</b>'
               '\n- Depan (wajah penuh),'
               '\n- Profil kiri (90 derajat)'
               '\n- Profil kanan'
               '\n- Pojok kiri (~45 derajat)'
               '\n- Pojok kanan'

               '\n\nAnda dapat mengklik /help untuk melihat semua perintah yang tersedia'
               '\nSebelum melanjutkan, harap baca <b>kebijakan privasi</b> kami dan klik tombol ✅.',
      'lang_ok': 'Bahasa disetel ke {}\nUntuk melihat daftar perintah, tekan /help',
      'pol_agree': 'Saya telah membaca dan menyetujui kebijakan',
      'instuct_agree': 'Saya telah membaca persyaratannya',
      'ban': 'Akses Anda ke tugas diblokir.',
      'vert': 'Anda perlu memotret secara vertikal, bukan horizontal. Tolong ulangi.',
      'horiz': 'Anda perlu memotret secara horizontal, bukan vertikal. Tolong ulangi.',
      'big_file': 'File yang lebih berat dari 50 Megabyte tidak diterima.',
      'small_file': 'Berat file hanya {} MB, kualitasnya terlalu rendah. Silakan ambil gambar dengan kualitas tinggi.',
      'privacy_missing': 'Klik kotak centang untuk menyetujui kebijakan privasi.',
      'instruct1': 'Anda memerlukan orang kedua untuk membuat film karena kami memerlukan jarak sekitar 1m.'
                   'Periksa <b>persyaratan</b> untuk file yang diunggah:\n'
                   '\n<u>1. Bersihkan Kamera</u>: Pastikan lensa tidak kotor.'
                   '\n<u>2. Resolusi dari 4K</u>: Setidaknya 2100x3800 piksel. Anda perlu memotret dengan kamera ponsel utama, bukan kamera selfie.'
                   '\n<u>3. Wajah terbuka:</u> Wajah Anda di foto benar-benar terbuka, tidak ditutupi atau dipotong.'
                   '\n<u>4. Pencahayaan bagus:</u> Tidak ada silau, silau pada wajah, atau penggelapan. Cahaya putih atau kuning.'
                   '\n<u>5. Orang luar:</u> Tidak boleh ada orang lain di dalam bingkai (baik yang hidup maupun yang ada di gambar), bahkan rambut atau tangan mereka pun tidak.'
                   '\n<u>6. Pembuatan film:</u> Filter/efek/masker apa pun dilarang.'
                   '\n<u>7. Dilarang di kepala:</u> headphone, masker, kacamata hitam, penutup kepala (kecuali yang bersifat keagamaan).'
                   '\n<u>8. Refleksi:</u> Tidak boleh ada cermin atau objek lain di latar belakang atau di dekat Anda di mana Anda akan dipantulkan.'
                   '\n<u>9. Latar Belakang:</u> Latar belakang polos sederhana tanpa banyak kekacauan, hanya dinding polos saja sudah sempurna.',

     'example': 'Contoh semua 15 gambar',
     'full_hd': 'Anda perlu mengirim file <b>tidak terkompresi</b>. Jika Anda tidak tahu caranya, maka'
                 ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">lihat contohnya</a> (9 detik).',
      'instruct2': 'Anda dapat memulai - tekan perintah /next dan bot akan menampilkan tugas selanjutnya, lalu ambil fotonya dan kirimkan ke chat ini.',
      'album': 'Kirim file satu per satu, jangan berkelompok',
      'receive': 'File yang diterima untuk tugas {}.\nTekan /next untuk tugas selanjutnya',
     'all_sent': 'Terima kasih! Anda telah mengirimkan semua file yang diperlukan. Harap tunggu hingga karya Anda ditinjau.\n'
                  'Tekan perintah /personal untuk menunjukkan jenis kelamin dan usia Anda, jika Anda belum menentukannya.',
      'no_more': 'Tidak ada tugas yang tersedia',
      'reject': 'Kami telah memeriksa pekerjaan Anda. Sayangnya, beberapa file tidak lulus ujian. Lihat '
                'komentar dan tekan /next untuk mendapatkan tugas.'
                '\nBerikutnya di setiap baris adalah nomor tugas yang salah diselesaikan dan komentarnya:',
    'block': 'Your assignment is rejected without an option to redo.',
    'reject_all': 'Kami telah memeriksa pekerjaan Anda. Sayangnya semua berkas tidak lulus ujian. '
                    'Silakan baca komentar kami di bawah dan tekan /next untuk mendapatkan tugas.',
      'all_approved': 'Sukses! Photo Anda berhasil melewati pemeriksaan kualitas pertama.\n'
                      'Dalam 1-2 hari kami akan memeriksa pekerjaan Anda lebih teliti. Koreksi baru mungkin perlu dilakukan. '
                      'Jika semuanya dilakukan dengan benar, orang yang menerima undangan tersebut akan menghubungi Anda. Identitas Anda: ',

      #pd
      'age': 'Tunjukkan usia Anda - dua angka bersamaan',
      'age_bad': 'Format tidak valid, saya perkirakan dua digit',
      'gender': 'Tunjukkan jenis kelamin Anda. Kirim satu huruf: m (pria) atau f (wanita)',
      'gender_bad': 'Format tidak valid, saya mengharapkan satu huruf Latin: m atau f',
      'race': 'Silahkan ikut lomba Anda',
      'fio': 'Silakan masukkan nama lengkap Anda',
      'fio_bad': 'Format tidak valid, saya mengharapkan dua atau tiga kata',
      'country': 'Tuliskan negara tempat tinggal Anda',
      # 'fio_bad': 'Format tidak valid, saya mengharapkan dua atau tiga kata',
      'pd_ok': 'Data Anda telah disimpan.',

      'tlk_ok': 'Data Anda telah disimpan. '
                'Masukkan data berikut ke antarmuka tugas Toloka (sentuh saja untuk menyalin):'
                '\n\nId-Telegram: <code>{}</code>'
                '\n\nKode verifikasi: <code>{}</code>'
    ,
}