# sync_delete

İki veya daha fazla senkronize klasör arasında otomatik dosya silici.

Elimdeki daha büyük projelere başlamamak için kendi kendime uydurduğum bir ihtiyacı karşılamak için bir gün gibi bir sürede kodladığım bir mini projedir kendileri. 

Eğer SyncBack ya da rsync gibi bir klasör senkronizasyon aracı kullanıyorsanız senkronize klasörlerden birinde dosya silmek çok can sıkıcı oluyor. 

Ya gidip diğer klasörden de dosyayı elle silmeniz gerekiyor, ya da senkronizasyon yazılımına her seferinde diğer klasörde bulunamayan dosya acaba silindi mi, yoksa mevcut olduğu klasörde yeni mi oluşturuldu söylemeniz gerek, çünkü senkronizasyon yazılımları bunu bilemiyor (genellikle dosyaları geriye doğru takip etmediklerinden). Dosya herhangi bir tarafta yoksa senkronizasyon esnasında diğer klasörden otomatik olarak kopyalanıyor. 

Bu durumu engellemek için aha da bu basit betiği yazdım. 

Bir dosyayı veya klasörü silmek yerine, ismini değiştirip dosya / klasör adının sonuna, önceden belirli bir sonek (suffix) koyuyorsunuz (öntanımlı değeri *__del*, ama betik içinden değiştirebilirsiniz). 

Betik, tanımlı tüm kök dizinler içerisinde tanımlı soneke sahip dosya ve klasörleri tarar. Bulduklarını hafızaya alarak diğer tüm kök dizinler içinde,aynı konumda bulunan dosyaları da tarayıp her birini, ait oldukları kök dizin içerisinde *_deleted* klasörünün içine taşır. İlaveten, ne zaman silindiklerini görebilmeniz için, dosya isimlerinin sonuna, dosyanın silindiği (aslında taşındığı) tarih ve saati de ekler. 

Dosyaların taşınacağı klasörü de (öntamınlı *_deleted*), betik içerisinden değiştirebilirsiniz. 

İsmiyle çelişiyor olabilir ama bu betik hiçbir dosyanızı silmez, yalnızca onları belirteceğiniz kök dizinler içindeki ayrı bir klasöre taşır. O yüzden bu metinde ve kod içindeki açıklamalardaki silmek ifadelerini taşımak diye okuyabilirsiniz. 

Parametrelerin detayları, betik dosyasının içinde kod açıklamaları halinde görülebilmekte ve tarafınızca değiştirilebilmektedir. 

Kod, Windows işletim sisteminde test edilmiştir. *nix ve Os X için test etmedim, ama tüm dosya işlemleri için python kütüphanelerini kullandığımdan dolayı sorunsuz çalışacaktır diye düşünüyorum. 

Herhangi bir soru veya sorununuz olursa Twitter hesabımdan (@SercioSoydanov) veya eposta ile (sercan.sydn@gmail.com) ulaşabilirsiniz. 

# Kullanımı

Ben şahsen iki makinem arasında dosya senkronizasyonu için SyncBack kullanıyorum, ki kendisinin *Programs - Before* denilen çok şık bir işlevi var. Her bir senkronizasyondan önce veya sonra çalışmak üzere bir betik veya program tanımlayabiliyorsunuz. Ben bu scripti, senkronizasyon profilimden önce çalışmaya programladım. SyncBack de sağolsun beni kırmıyor ve her çalışmadan önce betiği çalıştırıyor böylece hoop! Silinecek dosyalar *_deleted* klasörüne taşınmış oluyor. Yahşi. 

# Dosya Taşıma / Yeniden Adlandırma

Dosyaları yeniden adlandırırken / taşırken dikkat edin, çünkü bu basit betik dosya isimlendirme / taşıma işlemlerini takip etmiyor. Hoş bir özellik olurdu ama onu yapmak için tamamen farklı bir mimari ve çok daha üst seviye bir tasarım gerekir. 

Ayrıca bildiğim kadarıyla dosyaların ismi değiştiğinde, benzersiz tanımlayıcı ile takip edebilecek bir Python kütüphanesi yok (ancak yanılıyor olabilirim). 

Bu iş ancak işletim sisteminin yerel api çağrıları ile yapılabilir. Eğer ilğileniyorsanız Windows'un *GetFileInformationByHandle* fonksiyonuna ait kılavuz sayfasını aha da buraya bırakıyorum: 

https://docs.microsoft.com/tr-tr/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle?redirectedfrom=MSDN

