��    +      t  ;   �      �  ,   �  %   �          ,     L     X     e     l     �  �   �  g   2     �     �  '   �  �   �     �     �  �  �  -   {  o   �  m   	  i   �	  n   �	     `
     g
  �  �
     V     [     u  x   �             �   ,  :        @  ;   Z  e   �  �   �     �  
   �  6     *   ;  �  f  Q   5  B   �  6   �  D        F  %   Z     �  0   �  2   �  �   �     �     2     ?  E   N    �     �     �    �  D   �  �   ?  �     �   �  �   �     H  &   U  2  |     �   >   �   "   �   �   !  6   �!  #   �!    "  �   ##  *   �#  �   �#  �   P$  �  �$     t&  !   �&  u   �&  (   '                  (                             '                
           %         !             "      	                                   &          )                   $           *      #       +       %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Error Examples Executables (*.exe)|*.exe|All Files|*.* Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Plugin] ExternalTools ExternalTools plug-in allows to open the notes files with external applications.

The plug-in adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allows to run many applications. Every application must be placed at the separated lines.

If a line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
 ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul> Link Open Content File with... Open Result HTML File with... Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Open file dialog... Remove tool Run a lot of applications:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul> Title Tools List Warn before executing applications by (:exec:) command http://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: externaltools
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2018-01-30 09:26+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: jenyay.net <jenyay.ilin@gmail.com>
Language: ru_RU
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Poedit-KeywordsList: _;gettext;gettext_noop
X-Poedit-Basepath: ../../..
X-Poedit-SourceCharset: utf-8
X-Generator: Poedit 2.0.4
X-Poedit-SearchPath-0: .
 %attach%. Путь до текущей папки вложенных файлов %folder%. Путь до папки текущей страницы %html%. Текущая страница. Файл HTML %page%. Текущая страница. Текстовый файл Все файлы|* Добавить приложение Кнопка Ошибка запуска приложения Ошибка сохранения настроек Создать ссылку для запуска application.exe с параметрами:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Создание ссылки для запуска application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Ошибка Примеры Выполняемые файлы (*.exe)|*.exe|Все файлы|*.* Запустить application.exe из папки с прикрепленынми файлами:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
или
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Плагин] ExternalTools Плагин ExternalTools позволяет открывать файлы заметок во внешних приложениях.

Плагин добавляет команду (:exec:) для создания ссылки или кнопки, позволяющие запускать внешние приложения с викистраниц..

Команда (:exec:) позволяет запускать несколько приложений одновременно. Каждое приложение должно располагаться на отдельной строке.

Если строка начинается со знака "#", то эта строка игнорируется. Знак "#" в начале строки - это знак комментария.
 Плагин ExternalTools. Вставить команду (:exec:) Плагин ExternalTools. Вставить макрос %attach%. Этот макрос будет заменен на путь до папки с вложенными файлами текущей страницы. Плагин ExternalTools. Вставить макрос %folder%. Этот макрос будет заменен на путь до папки текущей страницы. Плагин ExternalTools. Вставить макрос %html%. Этот макрос будет заменен на путь до файла HTML текущей страницы. Плагин ExternalTools. Вставить макрос %page%. Этот макрос будет заменен на путь до текстового файла текущей страницы. Формат Вставка команды (:exec:) Внутри команды (:exec:) могут использоваться макросы. Эти макросы будут заменены на соответствующие пути:
<ul>
<li><b>%page%</b>. Этот макрос будет заменен на полный путь до файла с текстом страницы.</li>
<li><b>%html%</b>. Этот макрос будет заменен на полный путь до HTML-файла страницы.</li>
<li><b>%folder%</b>. Этот путь будет заменен на полный путь до папки страницы.</li>
<li><b>%attach%</b>. Этот макрос будет заменен на полный путь до папки с прикрепленными файлами без слеша на конце.</li>
</ul> Ссылка Открыть файл с текстом заметки в... Открыть HTML-файл в... Открыть прикрепленный файл с помощью application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Открыть диалог выбора файла... Удалить приложение Запуск нескольких приложений:
<code><pre>(:exec title="Запустить application_1, application_2 и application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Запустить приложение с помощью плагина ExternalTools?
Это может быть опасно. Запуск приложений (:exec:) Запустить приложения с помощью плагина ExternalTools?
Это может быть опасно. То же самое, но для создания кнопки
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> Команда (:exec:) имеет следующие необязательные параметры:
<ul>
<li>format. Если этот параметр равен "button", то команда создаст кнопку вместо ссылки (по умолчанию).</li>
<li>title. Этот параметр устанавливает текст для ссылки или кнопки.</li>
</ul> Заголовок Список приложений Предупреждать перед запуском приложений с помощью команды (:exec:) http://jenyay.net/Outwiker/ExternalTools 