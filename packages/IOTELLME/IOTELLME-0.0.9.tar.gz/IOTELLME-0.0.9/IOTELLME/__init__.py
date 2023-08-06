import requests
import json
class IOTELLME():
    def Token(self,token,users_id):
        if(isinstance(users_id, int)==True ):
            self.url = f'https://iotellme.cloud/api/send?token={token}&users_id={users_id}'
            self.write=self.url
            #read
            self.read_url = f'https://iotellme.cloud/api/read?token={token}&users_id={users_id}'
            self.read=self.read_url

    def Write1(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id1="+str(id)+"&v1="+str(v)+"&s1="+str(s)
            
    def Write2(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write + "&id2="+str(id)+"&v2="+str(v)+"&s2="+str(s)

    def Write3(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id3="+str(id)+"&v3="+str(v)+"&s3="+str(s)

    def Write4(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id4="+str(id)+"&v4="+str(v)+"&s4="+str(s)

    def Write5(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id5="+str(id)+"&v5="+str(v)+"&s5="+str(s)

    def Write6(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id6="+str(id)+"&v6="+str(v)+"&s6="+str(s)

    def Write7(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id7="+str(id)+"&v7="+str(v)+"&s7="+str(s)

    def Write8(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id8="+str(id)+"&v8="+str(v)+"&s8="+str(s)

    def Write9(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id9="+str(id)+"&v9="+str(v)+"&s9="+str(s)

    def Write10(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id10="+str(id)+"&v10="+str(v)+"&s10="+str(s)

    def Write11(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id11="+str(id)+"&v11="+str(v)+"&s11="+str(s)

    def Write12(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id12="+str(id)+"&v12="+str(v)+"&s12="+str(s)

    def Write13(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id13="+str(id)+"&v13="+str(v)+"&s13="+str(s)

    def Write14(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id14="+str(id)+"&v14="+str(v)+"&s14="+str(s)

    def Write15(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id15="+str(id)+"&v15="+str(v)+"&s15="+str(s)

    def Write16(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id16="+str(id)+"&v16="+str(v)+"&s16="+str(s)

    def Write17(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id17="+str(id)+"&v17="+str(v)+"&s17="+str(s)

    def Write18(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id18="+str(id)+"&v18="+str(v)+"&s18="+str(s)

    def Write19(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id19="+str(id)+"&v19="+str(v)+"&s19="+str(s)

    def Write20(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id20="+str(id)+"&v20="+str(v)+"&s20="+str(s)

    def Write21(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id21="+str(id)+"&v21="+str(v)+"&s21="+str(s)

    def Write22(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id22="+str(id)+"&v22="+str(v)+"&s22="+str(s)

    def Write23(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id23="+str(id)+"&v23="+str(v)+"&s23="+str(s)

    def Write24(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id24="+str(id)+"&v24="+str(v)+"&s24="+str(s)

    def Write25(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id25="+str(id)+"&v25="+str(v)+"&s25="+str(s)

    def Write26(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id26="+str(id)+"&v26="+str(v)+"&s26="+str(s)

    def Write27(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id27="+str(id)+"&v27="+str(v)+"&s27="+str(s)

    def Write28(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id28="+str(id)+"&v28="+str(v)+"&s28="+str(s)

    def Write29(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id29="+str(id)+"&v29="+str(v)+"&s29="+str(s)

    def Write30(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id30="+str(id)+"&v30="+str(v)+"&s30="+str(s)

    def Write31(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id31="+str(id)+"&v31="+str(v)+"&s31="+str(s)

    def Write32(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id32="+str(id)+"&v32="+str(v)+"&s32="+str(s)

    def Write33(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id33="+str(id)+"&v33="+str(v)+"&s33="+str(s)

    def Write34(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id34="+str(id)+"&v34="+str(v)+"&s34="+str(s)

    def Write35(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id35="+str(id)+"&v35="+str(v)+"&s35="+str(s)

    def Write36(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id36="+str(id)+"&v36="+str(v)+"&s36="+str(s)

    def Write37(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id37="+str(id)+"&v37="+str(v)+"&s37="+str(s)
    def Write38(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id38="+str(id)+"&v38="+str(v)+"&s38="+str(s)

    def Write39(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id39="+str(id)+"&v39="+str(v)+"&s39="+str(s)

    def Write40(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id40="+str(id)+"&v40="+str(v)+"&s40="+str(s)

    def Write41(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id41="+str(id)+"&v41="+str(v)+"&s41="+str(s)

    def Write42(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id42="+str(id)+"&v42="+str(v)+"&s42="+str(s)

    def Write43(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id43="+str(id)+"&v43="+str(v)+"&s43="+str(s)

    def Write44(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id44="+str(id)+"&v44="+str(v)+"&s44="+str(s)

    def Write45(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id45="+str(id)+"&v45="+str(v)+"&s45="+str(s)

    def Write46(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id46="+str(id)+"&v46="+str(v)+"&s46="+str(s)

    def Write47(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id47="+str(id)+"&v47="+str(v)+"&s47="+str(s)

    def Write48(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id48="+str(id)+"&v48="+str(v)+"&s48="+str(s)

    def Write49(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id49="+str(id)+"&v49="+str(v)+"&s49="+str(s)

    def Write50(self,id,v,s=0):
        if(isinstance(id, int)==True and (isinstance(v, int)==True or isinstance(v, float)==True) and isinstance(s, int)==True):
            self.write= self.write+ "&id50="+str(id)+"&v50="+str(v)+"&s50="+str(s)

########################################################################################################
    def Read1(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id1={id}'

    def Read2(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id2={id}'

    def Read3(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id3={id}'

    def Read4(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id4={id}'

    def Read5(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id5={id}'

    def Read6(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id6={id}'

    def Read7(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id7={id}'

    def Read8(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id8={id}'

    def Read9(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id9={id}'

    def Read10(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id10={id}'

    def Read11(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id11={id}'

    def Read12(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id12={id}'

    def Read13(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id13={id}'

    def Read14(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id14={id}'

    def Read15(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id15={id}'

    def Read16(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id16={id}'

    def Read17(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id17={id}'

    def Read18(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id18={id}'

    def Read19(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id19={id}'

    def Read20(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id20={id}'

    def Read21(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id21={id}'

    def Read22(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id22={id}'

    def Read23(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id23{id}'

    def Read24(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id24={id}'

    def Read25(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id25={id}'

    def Read26(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id26={id}'

    def Read27(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id27={id}'

    def Read28(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id28={id}'

    def Read29(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id29={id}'

    def Read30(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id30={id}'

    def Read31(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id31={id}'

    def Read32(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id32={id}'

    def Read33(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id33={id}'

    def Read34(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id34={id}'

    def Read35(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id35={id}'

    def Read36(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id36={id}'

    def Read37(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id37={id}'

    def Read38(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id38={id}'

    def Read39(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id39={id}'

    def Read40(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id40={id}'

    def Read41(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id41={id}'

    def Read42(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id42={id}'

    def Read43(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id43={id}'

    def Read44(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id404{id}'

    def Read45(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id45={id}'

    def Read46(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id46={id}'

    def Read47(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id47={id}'

    def Read48(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id48={id}'

    def Read49(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id49={id}'

    def Read50(self,id):
        if(isinstance(id, int)==True):
            self.read=self.read+f'&id50={id}'
    def Read(self):
        try:
            ressendbtn1 = requests.get(self.read)
            read= ressendbtn1.content
            self.R = json.loads(read)
        except Exception as e:
            print("No Internet Read")
            
    def Send(self):
        self.write= self.write 
        try:
            requests.get(self.write)
        except Exception as e:
            print("No Internet Send")

IOTELLME=IOTELLME()
