-- migrate:up

-- seeding countries table
-- downloaded from https://stefangabos.github.io/world_countries/
insert into countries(iso_2, iso_3, name) values
("af", "afg", "Afghanistan"),
("al", "alb", "Albanië"),
("dz", "dza", "Algerije"),
("ad", "and", "Andorra"),
("ao", "ago", "Angola"),
("ag", "atg", "Antigua en Barbuda"),
("ar", "arg", "Argentinië"),
("am", "arm", "Armenië"),
("au", "aus", "Australië"),
("az", "aze", "Azerbeidzjan"),
("bs", "bhs", "Bahama's"),
("bh", "bhr", "Bahrein"),
("bd", "bgd", "Bangladesh"),
("bb", "brb", "Barbados"),
("be", "bel", "België"),
("bz", "blz", "Belize"),
("bj", "ben", "Benin"),
("bt", "btn", "Bhutan"),
("bo", "bol", "Bolivia"),
("ba", "bih", "Bosnië en Herzegovina"),
("bw", "bwa", "Botswana"),
("br", "bra", "Brazilië"),
("bn", "brn", "Brunei"),
("bg", "bgr", "Bulgarije"),
("bf", "bfa", "Burkina Faso"),
("bi", "bdi", "Burundi"),
("kh", "khm", "Cambodja"),
("ca", "can", "Canada"),
("cf", "caf", "Centraal-Afrikaanse Republiek"),
("cl", "chl", "Chili"),
("cn", "chn", "China"),
("co", "col", "Colombia"),
("km", "com", "Comoren"),
("cg", "cog", "Congo-Brazzaville"),
("cd", "cod", "Congo-Kinshasa"),
("cr", "cri", "Costa Rica"),
("cu", "cub", "Cuba"),
("cy", "cyp", "Cyprus"),
("dk", "dnk", "Denemarken"),
("dj", "dji", "Djibouti"),
("dm", "dma", "Dominica"),
("do", "dom", "Dominicaanse Republiek"),
("de", "deu", "Duitsland"),
("ec", "ecu", "Ecuador"),
("eg", "egy", "Egypte"),
("sv", "slv", "El Salvador"),
("gq", "gnq", "Equatoriaal-Guinea"),
("er", "eri", "Eritrea"),
("ee", "est", "Estland"),
("et", "eth", "Ethiopië"),
("fj", "fji", "Fiji"),
("ph", "phl", "Filipijnen"),
("fi", "fin", "Finland"),
("fr", "fra", "Frankrijk"),
("ga", "gab", "Gabon"),
("gm", "gmb", "Gambia"),
("ge", "geo", "Georgië"),
("gh", "gha", "Ghana"),
("gd", "grd", "Grenada"),
("gr", "grc", "Griekenland"),
("gt", "gtm", "Guatemala"),
("gn", "gin", "Guinee"),
("gw", "gnb", "Guinee-Bissau"),
("gy", "guy", "Guyana"),
("ht", "hti", "Haïti"),
("hn", "hnd", "Honduras"),
("hu", "hun", "Hongarije"),
("ie", "irl", "Ierland"),
("is", "isl", "IJsland"),
("in", "ind", "India"),
("id", "idn", "Indonesië"),
("iq", "irq", "Irak"),
("ir", "irn", "Iran"),
("il", "isr", "Israël"),
("it", "ita", "Italië"),
("ci", "civ", "Ivoorkust"),
("jm", "jam", "Jamaica"),
("jp", "jpn", "Japan"),
("ye", "yem", "Jemen"),
("jo", "jor", "Jordanië"),
("cv", "cpv", "Kaapverdië"),
("cm", "cmr", "Kameroen"),
("kz", "kaz", "Kazachstan"),
("ke", "ken", "Kenia"),
("kg", "kgz", "Kirgizië"),
("ki", "kir", "Kiribati"),
("kw", "kwt", "Koeweit"),
("hr", "hrv", "Kroatië"),
("la", "lao", "Laos"),
("ls", "lso", "Lesotho"),
("lv", "lva", "Letland"),
("lb", "lbn", "Libanon"),
("lr", "lbr", "Liberia"),
("ly", "lby", "Libië"),
("li", "lie", "Liechtenstein"),
("lt", "ltu", "Litouwen"),
("lu", "lux", "Luxemburg"),
("mg", "mdg", "Madagaskar"),
("mw", "mwi", "Malawi"),
("mv", "mdv", "Malediven"),
("my", "mys", "Maleisië"),
("ml", "mli", "Mali"),
("mt", "mlt", "Malta"),
("ma", "mar", "Marokko"),
("mh", "mhl", "Marshalleilanden"),
("mr", "mrt", "Mauritanië"),
("mu", "mus", "Mauritius"),
("mx", "mex", "Mexico"),
("fm", "fsm", "Micronesië"),
("md", "mda", "Moldavië"),
("mc", "mco", "Monaco"),
("mn", "mng", "Mongolië"),
("me", "mne", "Montenegro"),
("mz", "moz", "Mozambique"),
("mm", "mmr", "Myanmar"),
("na", "nam", "Namibië"),
("nr", "nru", "Nauru"),
("nl", "nld", "Nederland"),
("np", "npl", "Nepal"),
("ni", "nic", "Nicaragua"),
("nz", "nzl", "Nieuw-Zeeland"),
("ne", "ner", "Niger"),
("ng", "nga", "Nigeria"),
("kp", "prk", "Noord-Korea"),
("mk", "mkd", "Noord-Macedonië"),
("no", "nor", "Noorwegen"),
("ug", "uga", "Oeganda"),
("ua", "ukr", "Oekraïne"),
("uz", "uzb", "Oezbekistan"),
("om", "omn", "Oman"),
("at","aut","Oostenrijk"),
("tl","tls","Oost-Timor"),
("pk","pak","Pakistan"),
("pw","plw","Palau"),
("pa","pan","Panama"),
("pg","png","Papoea-Nieuw-Guinea"),
("py","pry","Paraguay"),
("pe","per","Peru"),
("pl","pol","Polen"),
("pt","prt","Portugal"),
("qa","qat","Qatar"),
("ro","rou","Roemenië"),
("ru","rus","Rusland"),
("rw","rwa","Rwanda"),
("kn","kna","Saint Kitts en Nevis"),
("lc","lca","Saint Lucia"),
("vc","vct","Saint Vincent en de Grenadines"),
("sb", "slb", "Salomonseilanden"),
("ws", "wsm", "Samoa"),
("sm", "smr", "San Marino"),
("sa", "sau", "Saoedi-Arabië"),
("st", "stp", "Sao Tomé en Principe"),
("sn", "sen", "Senegal"),
("rs", "srb", "Servië"),
("sc", "syc", "Seychellen"),
("sl", "sle", "Sierra Leone"),
("sg", "sgp", "Singapore"),
("si", "svn", "Slovenië"),
("sk", "svk", "Slowakije"),
("sd", "sdn", "Soedan"),
("so", "som", "Somalië"),
("es", "esp", "Spanje"),
("lk", "lka", "Sri Lanka"),
("sr", "sur", "Suriname"),
("sz", "swz", "Swaziland"),
("sy", "syr", "Syrië"),
("tj", "tjk", "Tadzjikistan"),
("tz", "tza", "Tanzania"),
("th", "tha", "Thailand"),
("tg", "tgo", "Togo"),
("to", "ton", "Tonga"),
("tt", "tto", "Trinidad en Tobago"),
("td", "tcd", "Tsjaad"),
("cz", "cze", "Tsjechië"),
("tn", "tun", "Tunesië"),
("tr", "tur", "Turkije"),
("tm", "tkm", "Turkmenistan"),
("tv", "tuv", "Tuvalu"),
("uy", "ury", "Uruguay"),
("vu", "vut", "Vanuatu"),
("ve", "ven", "Venezuela"),
("ae", "are", "Verenigde Arabische Emiraten"),
("us", "usa", "Verenigde Staten"),
("gb", "gbr", "Verenigd Koninkrijk"),
("vn", "vnm", "Vietnam"),
("by", "blr", "Wit-Rusland"),
("zm", "zmb", "Zambia"),
("zw", "zwe", "Zimbabwe"),
("za", "zaf", "Zuid-Afrika"),
("kr", "kor", "Zuid-Korea"),
("ss", "ssd", "Zuid-Soedan"),
("se", "swe", "Zweden"),
("ch", "che", "Zwitserland")

-- migrate:down