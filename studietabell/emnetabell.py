import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict
import json
import pandas as pd
import re
from datetime import datetime
#må kanskje hente inn eier nivå#

# Brukernavn og passord
username = "uib_studieelementer_les1"
password = "Foiv;OvyicIjceg2"

# Funksjon for å utføre GraphQL-spørringen med autentisering
def run_query(query, username, password, variables=None):
    url = "https://api.fellesstudentsystem.no/graphql/"
    headers = {
        "Content-Type": "application/json", 
        "Feature-Flags": "beta,experimental"
        }
    auth = HTTPBasicAuth(username, password)
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
'''
defquery = """
{
  __schema {
    types {
      name
      kind
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
"""
result = run_query(defquery, username, password)
data = result
# Filtrer etter en bestemt type
target_type = "KullTerminbetegnelse"  # Endre til den typen du leter etter

filtered_types = [
    t for t in data["data"]["__schema"]["types"]
    if t["name"] == target_type
]

# Skriv ut resultatet
if filtered_types:
    print(filtered_types[0])  # Viser detaljer om den spesifikke typen
else:
    print(f"Ingen treff for typen {target_type}")



query = """
{
  __schema {
    types {
      name
      kind
      enumValues {
        name
      }
    }
  }
}
"""

response = run_query(query, username, password)
data = response

# Filtrer ut ENUM-typer
enum_types = [t for t in data["data"]["__schema"]["types"] if t["kind"] == "ENUM"]

print(enum_types)  # Viser tilgjengelige ENUM-typer
'''


def hent_id_for_terminbetegnelse(terminbetegnelse = None):
    # Gå gjennom listen 'edges' for å finne "HØST"
    data = run_query(terminbetegnelsequery, username, password)

    for edge in data['data']['terminbetegnelser']['edges']:
        if edge['node']['kode'] == terminbetegnelse:
            return edge['node']['id']
    return None

terminbetegnelsequery = """
{
    terminbetegnelser(filter: {eierOrganisasjonskode: "184"}) {
        edges {
            node {
                id
                kode
            }
        }
    }
}
"""

terminquery = """
query MyQuery($arstall: [Int!], $terminbetegnelser: [ID!]) {
  terminer(
    filter: {eierOrganisasjonskode: "184", arstall: $arstall, terminbetegnelser: $terminbetegnelser}
  ) {
    edges {
      node {
        id
        betegnelse {
          kode
          id
        }
        arstall
      }
    }
  }
}


terminbetegnelse = hent_id_for_terminbetegnelse('VÅR')
arstall = 2018
variables = {"arstall": arstall, "terminbetegnelser": terminbetegnelse}

result = run_query(terminquery, username, password, variables)
print(result)
quit()
"""
from bs4 import BeautifulSoup
soup_nav = BeautifulSoup('''''', '''html.parser''')
tab_tag = soup_nav.new_tag("div")
tab_tag.attrs['class']='tab'
soup_nav.append(tab_tag)

ar=[2024,2023,2022,2021,2020,2019,2018]
maxar = max(ar)

for arstall in ar:
  ar_tab_tag = soup_nav.new_tag("button")
  if arstall == maxar:
    ar_tab_tag.attrs['class']='tablinks active'
  if arstall != maxar:
    ar_tab_tag.attrs['class']='tablinks'
  ar_tab_tag.string=f'''{arstall}'''
  ar_tab_tag.attrs['onclick']=f'''valgtArstallKull(event, '{arstall}')'''
  find_tag_tag = soup_nav.find(class_='tab')
  find_tag_tag.append(ar_tab_tag)

  studieprogramkoder = ["BASV-GEOG",
  "BASV-SANT",
  "BASV-AORG",
  "BASV-INFO",
  "BASV-MEVI",
  "BASV-SAPO",
  "BASV-IKT",
  "BASV-EUR",
  "BASV-GOV",
  "BASV-JOU",
  "BASV-MIX",
  "BASV-TVP",
  "BASV-AIKI",
  "BASV-SØK",
  "PROF-SØK",
  "MASV-ITØK",
  "BASV-KOGNI",
  "BASV-SOS",
  "MASV-LÆSF"
  ]
 
  def artermin(arstall, terminbetegnelse):
      termin = 0
      if terminbetegnelse[0] == 'H':
          termin = 2
      if terminbetegnelse[0] == 'V':
          termin = 1
      arterminkode = f'''{arstall}{termin}'''
      return arterminkode

  terminbetegnelse = 'HOST'

  programkullartermin = artermin(arstall, terminbetegnelse)


  #Inneværende år
  innevar = datetime.now().year
  innevdato = datetime.now()

  # Sjekk om vi er før 1. juli
  termin = 1 if innevdato.month < 7 else 2
  innevartermin = f'''{innevar}{termin}'''


  filer = []

  query = """
  query MyQuery($cursor: String, $studieprogramkode: String!, $arstall: Int!, $betegnelse: KullTerminbetegnelse!) {
    studieoppbygninger(
      filter: {eierOrganisasjonskode: "184", kull: {arstall:  $arstall, betegnelse: $betegnelse, studieprogramkode: $studieprogramkode}}, after: $cursor
    ) {
      edges {
        node {
          alleOppbygningsdeler {
            rekkefolgenummer
            studieoppbygningsdel {
              kode
              navnAlleSprak {
                nb
              }
              vektingskrav {
                minimumsvekting {
                  verdi
                }
              }
              beskrivelseAlleSprak {
                nb
              }
              veivalg {
                harVeivalg
                antallVeivalg
              }
              utdanningsplanelementer {
                utdanningsplanelement {
                  kode
                }
                terminForPlasseringIUtdanningsplan {
                  terminnummerFra
                  terminnummerTil
                }
              }
              emner {
                emne {
                  kode
                  vekting {
                    emnevekting {
                      verdi
                    }
                  }
                  navnAlleSprak {
                    nb
                  }
                }
                kullterminer {
                  tilKullTermin {
                    arstall
                    betegnelse {
                      kode
                    }
                    id
                  }
                  fraKullTermin {
                    arstall
                    betegnelse {
                      kode
                    }
                    id
                  }
                }
                rekkefolgenummer
                sisteTerminForValg {
                  arstall
                  betegnelse {
                    kode
                  }
                  id
                }
                terminForPlasseringIUtdanningsplan {
                  terminnummerForhandsvalgt
                  terminnummerFra
                  terminnummerTil
                }
                valgregel {
                  kode
                  navnAlleSprak {
                    nb
                  }
                  erObligatorisk
                }
              }
            }
            kullterminer {
              kullStartFraTermin {
                id
                arstall
                betegnelse {
                  kode
                }
              }
              kullStartTilTermin {
                id
                arstall
                betegnelse {
                  kode
                }
              }
              sisteTerminForValg {
                arstall
                betegnelse {
                  kode
                }
                id
              }
            }
            terminNummerRelativStart
            parent {
              studieoppbygningsdel {
                kode
              }
              rekkefolgenummer
            }
          }
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
  """
  for studieprogramkode in studieprogramkoder:
    #test om det finnes informasjon for det studieprogrammet det året:
    kontroll_variables = {"cursor": None, "studieprogramkode": studieprogramkode, "arstall": arstall, "betegnelse": terminbetegnelse}
    kontroll_result = run_query(query, username, password, kontroll_variables)
    if not kontroll_result['data']['studieoppbygninger']['edges']:
      continue 
    print(studieprogramkode,arstall)

    filnavn = f'''{studieprogramkode}-{arstall}{terminbetegnelse[0]}.html'''
    filbane = f'''C:/Users/tto036/OneDrive - University of Bergen/Documents/Visual Studio Code/studieløptabell/{filnavn}'''
    fil = {}
    # Variabel for å holde cursor
    cursor = None
    beskrivelse = []

    tabelldata = []
    
    # Hent alle sider med resultater
    while True:
        variables = {"cursor": None, "studieprogramkode": studieprogramkode, "arstall": arstall, "betegnelse": terminbetegnelse}
        result = run_query(query, username, password, variables)
        print('')

        studieoppbygninger = result['data']['studieoppbygninger']
        
        alleOppbygningsdeler = studieoppbygninger['edges'][0]['node']['alleOppbygningsdeler']
        #print(alleOppbygningsdeler)
        print('')
        print('')
        for bygningsdel in alleOppbygningsdeler:
            parent = 'TOPP'
            if bygningsdel['parent']:
                parent = bygningsdel['parent']['studieoppbygningsdel']['kode']
            #bygningsdel['parent']['rekkefolgenummer'] 
                
            emnekombinasjon = bygningsdel['studieoppbygningsdel']
            emnekombinasjon['eier'] = parent
            emnekombinasjon['rekkefolgenummer']=bygningsdel['rekkefolgenummer']
            emnekombinasjon['kullStartFraTermin'] = ''
            emnekombinasjon['kullStartTilTermin'] = ''
            emnekombinasjon['sisteTerminForValg'] = ''
            emnekombinasjon['kullterminer']=bygningsdel['kullterminer']
            
            
                

            
            tabelldata.append(emnekombinasjon)
            
            

          
        # Sjekk om det er flere sider
        if studieoppbygninger['pageInfo']['hasNextPage']:
            cursor = studieoppbygninger['pageInfo']['endCursor']
        else:
            break


    # Lag en ordbok for å samle elementene under sin eier
    hierarki = defaultdict(lambda: {'eier': None,
                                    'rekkefolgenummer':None, 
                                    'lvl':None,
                                    'kode': None,
                                    'navnAlleSprak': None,
                                    'beskrivelseAlleSprak': None,
                                    'vektingskrav': None,
                                    'veivalg': None,
                                    'kullterminer': [], 
                                    'terminNummerRelativStart': None,
                                    'emner': [],
                                    'utdanningsplanelementer': [],
                                    'underordnede': []
                                    })

    # Først lagre alle elementene i ordboken
    for element in tabelldata:
        kode = element['kode']
        hierarki[kode].update(element)
        


    print('')


    # Så plasser dem under sin eier
    strukturert_data = {}

    for element in tabelldata:
        kode = element['kode']
        eier = element['eier']

        if eier == 'TOPP':
            strukturert_data[kode] = hierarki[kode]
        else:
            hierarki[eier]['underordnede'].append(hierarki[kode])


    from bs4 import BeautifulSoup
    soup = BeautifulSoup('''''', '''html.parser''')
    html_tag = soup.new_tag("html")
    head_tag = soup.new_tag("head")
    html_tag.append(head_tag)
    soup.insert(0,html_tag)
    head_tag = soup.head

    link_tag = soup.new_tag("link")
    link_tag.attrs['rel']='stylesheet'
    link_tag.attrs['href']='styles.css'
    head_tag.append(link_tag)

    '''
    style_tag = soup.new_tag("style")
    style_tag.string = """
      *{
      text-indent:.6em;
      line-height:2em;
      color:#191919;
      text-decoration:none
    }
    #tabell {
      width: 650px;
      border: solid 1px #aaaaaa;
      margin:.5em
    }

    .valgstatus.O,
    .valgstatus.OBL {
      display: none;
    }

    .emnekombnavn {
      font-weight: bold;
      padding-top:2px;
      padding-bottom:2px;
      background-color: #f1eeea;

      text-indent: .6rem;
      margin: 0;
      font-size: inherit;
      
    }

    

    .veivalg>.emnekombnavn {
      font-style: italic;
      
    }

    .veivalg>div>.emnekombnavn {
      font-weight: bold;

    }

    .veivalg>div>.emnekombnavn {
      font-weight: bold;
    
    }
    a{
      display: block;
    }
    a:not(:last-child), div:not(:last-child) {
      border-bottom: 1px solid #aaaaaa;
    }
    a:hover {
      background-color: #faf9f8;
      text-decoration: underline;
    }
    .valgstatus {
      font-style: italic;
    }

    .veivalg>div * {
      text-indent: 1.6em
    }

    .emnekombnavn>* {
      text-indent: 1em
    }

    #tabell > div > .emnekombnavn {
      font-weight: bold;
      background-color:#e2ddd5;
      padding-top:2px;
      padding-bottom:2px

    }

  .emnekombnavn:not(:last-child){
    border-bottom: 1px solid #aaa;
  }


    .valgstatus{
      font-style: italic;
      text-indent: .6rem;
      margin: 0;
      font-size: inherit;
      border-bottom: 1px solid #aaaaaa;
      font-weight: unset;
      }

      
  .flex-container {
    display: flex;
  }

  .flex-container section {
    flex: 1; // By your image example it looks like you want this element to stretch
  }
  .flex-container aside {
    border-left:solid;
    width:300px;
  }
aside * {
      text-indent: 0;
      text-decoration:none
    }
button {
  background: none;
  border: none;
}
ul {
  list-style: none;
  padding-left: 1em;
}
.tab{
      padding-left: 0.7em;
}
    """

    head_tag.append(style_tag)
    '''
    script_tag1 = soup.new_tag("script")
    script_tag1.attrs['src']='include-html.min.js'
    head_tag.append(script_tag1)

    script_tag2 = soup.new_tag("script")
    script_tag2.string = '''function valgtArstallKull(evt, arstallKull) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(arstallKull).style.display = "block";
    evt.currentTarget.className += " active";
  }
  '''
    head_tag.append(script_tag2)

    body_tag = soup.new_tag("body")

    html_tag.append(body_tag)
    body_tag = soup.body
    
    flex_container = soup.new_tag("div")
    flex_container.attrs['class']='flex-container'
    flex_container.attrs['id']='flex-container'
    body_tag.insert(1,flex_container)
    
    find_flex_container = soup.find(id='flex-container')
    section_tag = soup.new_tag("section")
    section_tag.attrs['id']='section'
    
    find_flex_container.insert(1,section_tag)

    aside_tag = soup.new_tag("aside")
    aside_tag.attrs['id']='aside'
    

    find_flex_container.insert(2,aside_tag)

    data_include = soup.new_tag("div")
    data_include.attrs['data-include']='nav.html'
    find_aside = soup.find(id='aside')
    find_aside.insert(1,data_include)

    find_section = soup.find(id='section')
    div_table_tag = soup.new_tag("div")
    div_table_tag.attrs['id']='tabell'
    find_section.insert(1,div_table_tag)
    
    for t in tabelldata:
        
        kullterminer = t.get('kullterminer', {})
        kullStartFraTermin = '0'
        kullStartTilTermin = '999999'
        sisteTerminForValg = '999999'
        if kullterminer:  # Sjekker at kullterminer ikke er None
            if kullterminer.get('kullStartFraTermin'):
                ar = kullterminer.get('kullStartFraTermin').get('arstall')
                betegnelse = kullterminer.get('kullStartFraTermin').get('betegnelse').get('kode')
                betegnelse = betegnelse.replace('VÅR','1').replace('HØST','2')
                artermin = f'{ar}{betegnelse}'
                kullStartFraTermin = artermin
            
            if kullterminer.get('kullStartTilTermin'):
                ar = kullterminer.get('kullStartTilTermin').get('arstall')
                betegnelse = kullterminer.get('kullStartTilTermin').get('betegnelse').get('kode')
                betegnelse = betegnelse.replace('VÅR','1').replace('HØST','2')
                artermin = f'{ar}{betegnelse}'
                kullStartTilTermin = artermin
            
            if kullterminer.get('sisteTerminForValg'):
                ar = kullterminer.get('sisteTerminForValg').get('arstall')
                betegnelse = kullterminer.get('sisteTerminForValg').get('betegnelse').get('kode')
                betegnelse = betegnelse.replace('VÅR','1').replace('HØST','2')
                artermin = f'{ar}{betegnelse}'
                sisteTerminForValg = artermin
        if (int(programkullartermin) > int(kullStartFraTermin)) and (int(programkullartermin) < int(kullStartTilTermin)) and (int(innevartermin) < int(sisteTerminForValg)):
          
          id= t['kode']
          vekt = ''
          if t['vektingskrav']:
              if t['vektingskrav']['minimumsvekting']:
                vekt=f''' ({t['vektingskrav']['minimumsvekting']['verdi']} sp)'''
          tekst = f'''{t['navnAlleSprak']['nb']} {vekt}'''
          id = id.replace(" ", "-")
          tag = soup.new_tag('div')
          tag.attrs['id']=id
          tag.attrs['data-sort']='0'
          if t['rekkefolgenummer']:
            tag.attrs['data-sort']=t['rekkefolgenummer']
          

          valg = hierarki[t['kode']]['veivalg']
          if valg:
              if valg['harVeivalg']:
                  tag.attrs['class']='veivalg'
          
          if (studieprogramkode != 'BASV-EUR') and (t['navnAlleSprak']['nb'] =='Utveksling'):
            tag.attrs['style']='display: none;'
          
          find_table = soup.find(id='tabell')
          find_table.append(tag)  
          
          ntag = soup.new_tag('h3')
          ntag.attrs['class']='emnekombnavn'
          ntag.string = tekst
          
          parent_tag = soup.find(id=id)
          parent_tag.append(ntag)

          valgregler = [
              {'kode': e['valgregel']['kode'], 'navnAlleSprak': e['valgregel']['navnAlleSprak']['nb']}
              for e in t.get('emner', [])
              ]
          unike_valgregler_set = list({(v['kode'], v['navnAlleSprak']): v for v in valgregler}.values())

          for v in unike_valgregler_set:
              
              valgkode = v['kode']
              valgkode = valgkode.replace(" ", "-")
              id= t['kode']
              id = id.replace(" ", "-")
              valgid = f'{id}-{valgkode}'
              vtag = soup.new_tag('div')
              vtag.attrs['id']=valgid
              
              parent_tag = soup.find(id=id)
              parent_tag.append(vtag)

              tagvv = soup.find(id=valgid)
              tagv = soup.new_tag('h4')
              tagv.string = v['navnAlleSprak']
              tagv.attrs['class']=f'''valgstatus {v['kode']}'''
              tagvv.insert(0,tagv)
          
          for e in t.get('emner'):
            
            tilKullTermin = '999999'
            fraKullTermin = '0'
            kullterminer = e.get('kullterminer')
            if kullterminer:
              if kullterminer.get('kullStartFraTermin'):
                  ar = kullterminer.get('kullStartFraTermin').get('arstall')
                  betegnelse = kullterminer.get('kullStartFraTermin').get('betegnelse').get('kode')
                  betegnelse = betegnelse.replace('VÅR','1').replace('HØST','2')
                  artermin = f'{ar}{betegnelse}'
                  fraKullTermin = artermin
              
              if kullterminer.get('kullStartTilTermin'):
                  ar = kullterminer.get('kullStartTilTermin').get('arstall')
                  betegnelse = kullterminer.get('kullStartTilTermin').get('betegnelse').get('kode')
                  betegnelse = betegnelse.replace('VÅR','1').replace('HØST','2')
                  artermin = f'{ar}{betegnelse}'
                  tilKullTermin = artermin



            if e['sisteTerminForValg']:
              emnesisteTerminForValg = f'''{e['sisteTerminForValg']['arstall']}{e['sisteTerminForValg']['betegnelse']['kode']}'''.replace('HØST','2').replace('VÅR','1')
              

              if (int(emnesisteTerminForValg) >= int(innevartermin)) and (int(fraKullTermin) <= int(programkullartermin)) and (int(tilKullTermin) >= int(programkullartermin)):
                  
                  evalgkode = e['valgregel']['kode']
                  evalgkode = evalgkode.replace(" ", "-")
                  id= t['kode']
                  id = id.replace(" ", "-")
                  evalgid = f'{id}-{evalgkode}'
                  etag = soup.new_tag('a')  #div
                  if e['valgregel']['erObligatorisk']:
                      etag.attrs['class']='emne obl'
                  else:
                      etag.attrs['class']='emne valg'
                  etag.attrs['href']=f'''https://www4.uib.no/emner/{e['emne']['kode']}'''
                  etag.attrs['target'] = "_blank"
                  etag.string = f'''{e['emne']['kode']} - {e['emne']['navnAlleSprak']['nb']}'''
                  eparent_tag = soup.find(id=evalgid)
                  
                  eparent_tag.append(etag)
            elif (int(fraKullTermin) <= int(programkullartermin)) and (int(tilKullTermin) >= int(programkullartermin)):
                  evalgkode = e['valgregel']['kode']
                  evalgkode = evalgkode.replace(" ", "-")
                  id= t['kode']
                  id = id.replace(" ", "-")
                  evalgid = f'{id}-{evalgkode}'

                  etag = soup.new_tag('a')

                  if e['valgregel']['erObligatorisk']:
                      etag.attrs['class']='emne obl'
                  else:
                      etag.attrs['class']='emne valg'
                  etag.attrs['href']=f'''https://www4.uib.no/emner/{e['emne']['kode']}'''
                  etag.attrs['target'] = "_blank"
                  etag.string = f'''{e['emne']['kode']} - {e['emne']['navnAlleSprak']['nb']}'''
                  eparent_tag = soup.find(id=evalgid)
                  
                  eparent_tag.append(etag)

    
    #print(soup.prettify())
          
    #print (soup)
    print('------')

    tk = tabelldata[:]  # Lag en kopi for å unngå feil ved fjerning
    while tk:
        for t in tk[:]:  # Iterer over en kopi for å unngå problemer
            emnekombkode = t['kode'].replace(" ", "-")
            emnekomeier = t['eier'].replace(" ", "-")

            # Finn taggen som skal flyttes
            tag_to_move = soup.find(id=emnekombkode)
            if tag_to_move:
              if tag_to_move['data-sort']:
                  sort_value = int(tag_to_move['data-sort'])
              else:
                  sort_value=int(-1)
              # Finn destinasjonen
              destination = soup.find(id=emnekomeier)

              # Flytt taggen ved å fjerne den fra originalen og legge den til et annet sted
              if tag_to_move and destination:
                  tag_to_move.extract()  # Fjern fra originalen
                  
                  destination.insert(int(sort_value),tag_to_move)

              # Fjern elementet etter at det er behandlet
              #tk.remove(t)  
        tk.remove(t)  

    # Skriv ut det oppdaterte HTML-dokumentet
    #print(soup.prettify())
    print('')


    heading_tag = soup.new_tag('h1')
    heading_tag.string = f'''{studieprogramkode} {arstall} {terminbetegnelse.replace('O','Ø').replace('A','Å')}'''
    


    heading_destination = soup.find('body')      
    heading_destination.insert(0,heading_tag)
    program = soup.find(class_='emnekombnavn') 
    
    s_renset = re.sub(r"\s*\(\d+[^()]*\)$", "", program.string)

    fil['navn'] = s_renset
    fil['filnavn'] = filnavn
    fil['arstall'] = arstall
    filer.append(fil)
    with open(filbane, "w", encoding='utf-8') as file:
      file.write(str(soup))


  from bs4 import BeautifulSoup
  soup1 = BeautifulSoup('''''', '''html.parser''')
  div_tab = soup1.new_tag("div")
  div_tab.attrs['id']=arstall
  div_tab.attrs['class']='tabcontent'
  if arstall == maxar:
    div_tab.attrs['style']='display: block;'
  if arstall != maxar:
    div_tab.attrs['style']='display: none;'
  ul_tag = soup1.new_tag("ul")
  
  for f in filer:
      li_tag = soup1.new_tag("li")
      a_tag = soup1.new_tag("a")
      a_tag.string=f['navn']
      a_tag.attrs['href']=f['filnavn']
      li_tag.append(a_tag)
      ul_tag.append(li_tag)
      
  div_tab.append(ul_tag)
  soup1.insert(1,div_tab)
  soup_nav.append(soup1)

print(soup_nav.prettify())
filnavn = f'''nav.html'''
filbane = f'''C:/Users/tto036/OneDrive - University of Bergen/Documents/Visual Studio Code/studieløptabell/{filnavn}'''
with open(filbane, "w", encoding='utf-8') as file:
  file.write(str(soup_nav))