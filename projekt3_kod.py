#zaimportowanie bibliotek
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.mapview import MapView, MapMarker
from math import radians,sqrt, tan, atan, cos, sin, atan2

#wizualizacja wyglądu aplikacji
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Show me on the map'
            on_press: root.manager.current = 'showme'
        Button:
            text: 'Flags of world countries'
            on_press: root.manager.current = 'flags'

<ShowMeScreen>:
    search_lat: coor_lat
	search_long: coor_long
	my_map: map
	my_image: image
    my_score: score
    GridLayout:
        rows: 4
        cols: 1
        BoxLayout:
            orientation: 'horizontal'
            MapView:
                size_hint_x:50
			    lat: 0
			    lon: 0
			    zoom: 1
			    id: map
			    on_map_relocated:root.draw_marker()
            Image:
                size_hint_x:50
                source: 'paryz.jpg'
                id: image
        BoxLayout:
    		size_hint_y: 0.1
    		Label:
    			size_hint_x: 25
    			text: "Latitude"
    		TextInput:
                size_hint_x:25
                id:coor_lat
    		Label:
    			size_hint_x: 25
    			text: "Longitude"
    		TextInput:
    			size_hint_x: 25
    			id: coor_long
    	BoxLayout:
    		size_hint_y: 0.1
    		Label:
    			size_hint_x: 25
    			text: "Score"
    		TextInput:
    			size_hint_x: 25
    			id: score
    		Button:
    			size_hint_x: 25
    			text: "Check"
    			on_press: root.check_points()
    		Button:
    			size_hint_x: 25
    			text: "Next"
                on_press:root.next_photo()
        BoxLayout:
            size_hint_y: 0.1
            Button:
                height: "40dp"
                text: 'Back to menu'
                on_press: root.manager.current = 'menu'
            
<FlagsScreen>:
    my_image: image
    my_score1: score
    GridLayout:
        rows: 4
        BoxLayout:
            Image:
                source: 'anglia.jpg'
                id: image
        BoxLayout:
    		size_hint_y: 0.1
    		Label:
    			size_hint_x: 50
    			text: "Score"
    		TextInput:
    			size_hint_x: 50
    			id: score
        BoxLayout:
            size_hint_y: 0.1
            Button:
        		size_hint_x: 50
        		text: "Yes"
                on_press:root.next_photo_yes()
        	Button:
        		size_hint_x: 50
        		text: "No"
                on_press:root.next_photo_no()
        BoxLayout:
            size_hint_y: 0.1
            Button:
                height: "40dp"
                text: 'Back to menu'
                on_press: root.manager.current = 'menu'    
        
                    
                      
""")

# zadeklarowanie okna głównego
class MenuScreen(Screen):
    pass

# zadeklarowanie okna quiz "Show me on the map"
class ShowMeScreen(Screen):
    
    #sprawdzenie szerokosci geogr.
    def checkValueLat(self, lat):
        if lat.lstrip('-').replace('.','').isdigit():
            if float(lat)> -90 and float(lat)< 90:
                return float (lat)
    
    #sprawdzenie dlugosci geogr.
    def checkValueLon(self, lon):
        if lon.lstrip('-').replace('.','').isdigit():
            if float(lon)>= -180 and float(lon)<= 180:
                return float (lon)
    
    #funkcja rysujaca marker na mapie 
    def draw_marker(self):
        
        try:
            self.my_map.remove_marker(self.marker)
        except:
            pass
        
        #zadeklarowanie zmiennych
        self.score = self.my_score
        self.latitude = self.my_map.lat
        self.longitude = self.my_map.lon
        
        if self.latitude != None and self.longitude != None:
        
            self.marker = MapMarker(lat=self.latitude, lon=self.longitude)
            self.my_map.add_marker(self.marker)
            
            self.search_lat.text="{:5.5f}".format(self.latitude)
            self.search_long.text="{:5.5f}".format(self.longitude)
        
    #zadeklarowanie funkcji sprawdzającej
    def check_points(self):
        
        #algorytm Vincentego
        for i in range(0,10):
                if self.my_image.source==list_of_points[i][0]:
                            fiA=radians(list_of_points[i][1]);
                            lamA=radians(list_of_points[i][2]);
                            fiB=radians(self.latitude);
                            lamB=radians(self.longitude);
                            a = 6378137.000;
                            e2= 0.00669438002290;
                            b=a*sqrt(1-e2);
                            f=1-(b/a);
                            delta_lambda=radians(lamB-lamA)
                            Ua=atan((1-f)*tan(radians(fiA)))
                            Ub=atan((1-f)*tan(radians(fiB)))
                            L=delta_lambda;
                            iteracja=0
                            k=1
                            while k > (0.000001/206265):
                                iteracja=iteracja+1
                                l=L
                                sin_sigma=sqrt((cos(Ub)*sin(L))**2+(cos(Ua)*sin(Ub)-sin(Ua)*cos(Ub)*cos(L))**2);
                                cos_sigma=(sin(Ua)*sin(Ub))+ (cos(Ua)*cos(Ub)*cos(L));
                                sigma=atan2(sin_sigma,cos_sigma);
                                sin_alfa=(cos(Ua)*cos(Ub)*sin(L))/sin_sigma;
                                cos_alfa=sqrt(1-((sin_alfa)**2));
                                cos_alfa2=(cos_alfa)**2;
                                cos_2sigma_m=cos_sigma-((2*sin(Ua)*sin(Ub))/cos_alfa2);
                                C=(f/16)*cos_alfa2*((4+f*(4-3*cos_alfa2)));
                                L=delta_lambda+(1-C)*f*sin_alfa*(sigma+C*sin_sigma*(cos_2sigma_m+C*(cos_sigma*(-1+2*(cos_2sigma_m)**2))));
                                k=abs(l-L)
                            
                            u2=((a**2-b**2)/b**2)*cos_alfa2;
                            A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)));
                            B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)));
                            delta_sigma=(B*sin_sigma)*(cos_2sigma_m+(1/4)*B*(cos_sigma*(-1+2*((cos_2sigma_m)**2))-(1/6)*B*cos_2sigma_m*(-3+4*((sin_sigma)**2)*(-3+4*((cos_2sigma_m)**2)))))
                            S_AB=b*A*(sigma-delta_sigma)
                            print(S_AB)
                            
        #zadeklarowanie warunkow odleglosciowych
        if S_AB<10:
                self.score=100
                list_check.append(self.score)
        elif S_AB>=10 and S_AB<100:
                self.score=50
                list_check.append(self.score)
        elif S_AB>=100 and S_AB<1000:
                self.score=25
                list_check.append(self.score)
        elif S_AB>=1000 and S_AB<3000:    
                self.score=10
                list_check.append(self.score)
        elif S_AB>=3000 and S_AB<7000:
                self.score=5
                list_check.append(self.score)
        elif S_AB>7000:
                self.score=0
                list_check.append(self.score)

        #warunki sumujące punkty                 
        if self.my_image.source==list_of_points[0][0]:
                self.my_score.text="{:5}".format(list_check[0])
        elif self.my_image.source==list_of_points[1][0]:
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[2][0]:
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[3][0]:  
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[4][0]:  
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[5][0]: 
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[6][0]: 
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[7][0]: 
                self.my_score.text="{:5}".format(sum(list_check))
        elif self.my_image.source==list_of_points[8][0]: 
                self.my_score.text="{:5}".format(sum(list_check))

    # funkcja pozwalająca zmieniać zdjęcia   
    def next_photo(self):
            if self.my_image.source==list_of_points[0][0]:
                self.my_image.source=list_of_points[1][0]
            elif self.my_image.source==list_of_points[1][0]:
                self.my_image.source=list_of_points[2][0]
            elif self.my_image.source==list_of_points[2][0]:
                self.my_image.source=list_of_points[3][0]
            elif self.my_image.source==list_of_points[3][0]:  
                self.my_image.source=list_of_points[4][0]
            elif self.my_image.source==list_of_points[4][0]:  
                self.my_image.source=list_of_points[5][0]
            elif self.my_image.source==list_of_points[5][0]: 
                self.my_image.source=list_of_points[6][0]
            elif self.my_image.source==list_of_points[6][0]: 
                self.my_image.source=list_of_points[7][0]
            elif self.my_image.source==list_of_points[7][0]: 
                self.my_image.source=list_of_points[8][0]
            elif self.my_image.source==list_of_points[8][0]: 
                self.my_image.source=list_of_points[9][0]

#zadeklarowanie okna quiz "Flags of world countries"
class FlagsScreen(Screen):
    
    #zadeklarowanie funkcji działającej pod przycisk "Yes"
    def next_photo_yes(self):
        self.score = self.my_score1
        if self.my_image.source==list_of_countries[0][0]:
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(list_check1[0])
            self.my_image.source=list_of_countries[1][0]
        elif self.my_image.source==list_of_countries[1][0]:
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[2][0]
        elif self.my_image.source==list_of_countries[2][0]:
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[3][0]
        elif self.my_image.source==list_of_countries[3][0]:  
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[4][0]
        elif self.my_image.source==list_of_countries[4][0]:  
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[5][0]
        elif self.my_image.source==list_of_countries[5][0]: 
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[6][0]
        elif self.my_image.source==list_of_countries[6][0]: 
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[7][0]
        elif self.my_image.source==list_of_countries[7][0]:
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[8][0]
    
    #zadeklarowanie funkcji działającej pod przycisk "No"
    def next_photo_no(self):
        self.score = self.my_score1
        if self.my_image.source==list_of_countries[0][0]:
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(list_check1[0])
            self.my_image.source=list_of_countries[1][0]
        elif self.my_image.source==list_of_countries[1][0]:
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[2][0]
        elif self.my_image.source==list_of_countries[2][0]:
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[3][0]
        elif self.my_image.source==list_of_countries[3][0]:  
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[4][0]
        elif self.my_image.source==list_of_countries[4][0]:  
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[5][0]
        elif self.my_image.source==list_of_countries[5][0]: 
            self.score=5
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[6][0]
        elif self.my_image.source==list_of_countries[6][0]: 
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[7][0]
        elif self.my_image.source==list_of_countries[7][0]:
            self.score=0
            list_check1.append(self.score)
            self.my_score1.text="{:5}".format(sum(list_check1))
            self.my_image.source=list_of_countries[8][0]

# Stworzenie okna managera
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ShowMeScreen(name='showme'))
sm.add_widget(FlagsScreen(name='flags'))

#stworzenie list
list_of_points=[
                ['paryz.jpg',48.8534100,2.3488000],
                ['dubai.jpg',25.0657000,55.1712800],
                ['londyn.jpg',51.5085300,-0.1257400],
                ['moskwa.jpg',55.7522200,37.6155600],
                ['nowy_jork.jpg',40.6903030,-74.04575600],
                ['berlin.jpg',52.5243700,13.4105300],
                ['sydney.jpg',-33.8678500,151.2073200],
                ['tokio.jpg',35.6895000,139.6917100],
                ['warszawa.jpg',52.2297700,21.0117800],
                ['waszyngton.jpg',38.8951100, -77.0363700],
                ]
list_check=[]
list_check1=[]
list_of_countries=[
                   ['anglia.jpg'],
                   ['australia.jpg'],
                   ['chiny.jpg'],
                   ['hiszpania.jpg'],
                   ['niemcy.jpg'],
                   ['polska.jpg'],
                   ['rosja.jpg'],
                   ['usa.jpg'],
                   ['koniec.jpg'],
                   ]

class multipleScreens(App):

    def build(self):
        return sm

if __name__ == '__main__':
    multipleScreens().run()