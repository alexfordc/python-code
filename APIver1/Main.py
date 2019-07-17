# 系統套件
import sys
import os
import datetime
import time
#運算套件
import numpy as np
import pandas as pd
# 使用PyQt5套件
from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt,QThread,pyqtSignal #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidgetItem #PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
#匯入外部字寫套件
import FuncUI
import tickstokline
import KlineUi
# 使用SKCOM元件
import comtypes.client
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

class SKMainWindow(QMainWindow): #主視窗
    def __init__(self):
        super(SKMainWindow,self).__init__()
        loadUi(r'UI/MainWindow.ui',self)
        self.showMaximized()
        # 帳號處理
        self.SKID='未登入' # 
        self.statusBar.showMessage('帳號:'+self.SKID)
        self.Bill=[]
        # 介面導入
        self.SKLoginUI() #登入介面
        self.SKMessageFunc()#系統訊息介面
        self.RightUI() #權益數介面        
        #ManuBar連結
        self.actionLogin.triggered.connect(self.Login.show)#登入介面連結
        #ToolBar連結
        self.SysDetail.triggered.connect(self.SKMessage.show)
        self.Connectbtn.triggered.connect(self.ConnectFun)
        self.Disconnectbtn.triggered.connect(self.disconnectFun)

        # Tab內功能組連結
        self.commoditybtn.clicked.connect(self.commodityFnc)

    # 呼叫系統訊息介面與功能
    def SKMessageFunc(self):
        self.SKMessage=FuncUI.MessageDialog('系統訊息') #設定系統訊息介面        
        self.SKMessage.setWindowModality(QtCore.Qt.WindowModal)#設定須先關閉對話框，GUI設定無效
        # self.SKMessage.setWindowTitle('系統訊息')
    # 系統功能介面結束
    # 呼叫登入介面，與登入功能
    def SKLoginUI(self):
        self.Login=FuncUI.LoginDialog()
        self.Login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)#設定最上層
        self.Login.setWindowModality(QtCore.Qt.ApplicationModal)#設定須先完成對話框，GUI設定無效
        self.Login.show()
        self.Login.LoginConfirmbtn.clicked.connect(self.LoginFunc)
    
    def LoginFunc(self):
        try:
            skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Quote")
            ID=self.Login.LoginID.text().replace(' ','')
            PW=self.Login.LoginPW.text().replace(' ','')
            m_nCode = skC.SKCenterLib_Login(ID,PW)
            m_nCode = skO.SKOrderLib_Initialize()
            m_nCode = skO.GetUserAccount()
            if m_nCode==0:
                self.SKID=ID
                self.statusBar.showMessage('帳號:'+str(self.SKID))
                self.SKMessage.textBrowser.append('登入成功')
                self.SKMessage.textBrowser.append('帳號: '+str(self.SKID))
                self.Login.close()
            else:
                self.SKMessage.textBrowser.append('登入失敗,錯誤碼:')
                ID='未登入'
                pass
        except Exception as e:
            # messagebox.showerror("error！",e)
            self.SKMessage.textBrowser.append('發生錯誤:'+e)
            # print('系統錯誤:'+e)
            pass
    # 登入功能結束
    # 權益數介面
    def RightUI(self):
        self.Right_TB.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Right_TB.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Right_TB.setHorizontalHeaderLabels(['帳戶餘額','浮動損益','已實現費用'])

        self.Bill=pd.DataFrame(np.arange(39).reshape(39),columns=['Right']) # 期貨權益數
        # self.Bill['RightItem']=''
        i=0
        while i < self.Bill.shape[0]:
            self.Bill.loc[i,'Right']=QTableWidgetItem('')
            self.Bill.loc[i,'Right'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i+=1
        i=1
        j=0
        while i < self.Right_TB.rowCount():
            self.Right_TB.setItem(i,0,self.Bill.loc[j,'Right'])
            j+=1
            self.Right_TB.setItem(i,1,self.Bill.loc[j,'Right'])
            j+=1
            self.Right_TB.setItem(i,2,self.Bill.loc[j,'Right'])
            j+=1
            i+=2
    # 權益數介面結束    
    # 閃電下單
    def DomTableUI(self):
        self.DomTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DomTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DomTable.setHorizontalHeaderLabels(['買價','成交價','賣價'])
        self.bestfive=pd.DataFrame(np.arange(27).reshape(27),columns=['close'])
        self.bestfive['bid']=0
        self.bestfive['ask']=0
        self.bestfive=self.bestfive[['close','bid','ask']].astype(int)
        self.bestfive['closeTBitem']=''
        self.bestfive['bidTBitem']=''
        self.bestfive['askTBitem']=''
        self.lastclose=[]
        self.lastbidlist=[]
        self.lastasklist=[]
        # while i < self.bestfive.shape[0]:
        i=0
        while i < 27 :
            self.bestfive.loc[i,'closeTBitem']=QTableWidgetItem('')
            self.DomTable.setItem(i,1,self.bestfive.loc[i,'closeTBitem'])
            self.bestfive.loc[i,'bidTBitem']=QTableWidgetItem('')
            self.DomTable.setItem(i,0,self.bestfive.loc[i,'bidTBitem'])
            self.bestfive.loc[i,'askTBitem']=QTableWidgetItem('')
            self.DomTable.setItem(i,2,self.bestfive.loc[i,'askTBitem'])
            self.bestfive.loc[i,'closeTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i,'bidTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.bestfive.loc[i,'askTBitem'].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            i+=1    
        self.bestfive.loc[13,'closeTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13,'bidTBitem'].setBackground(Qt.yellow)
        self.bestfive.loc[13,'askTBitem'].setBackground(Qt.yellow)

    def DomTableFillFunc(self,nclose,bid_dict,ask_dict):
        if self.bestfive.loc[13,'close'] != nclose:
            self.bestfive['close']=self.bestfive['close'].map(lambda x : nclose+13-(self.bestfive['close'][self.bestfive['close']==x].index[0]))
            self.bestfive['closeTBitem'].map(lambda x:x.setText(str(self.bestfive.loc[self.bestfive['closeTBitem'][self.bestfive['closeTBitem']==x].index[0],'close'])))
        self.bestfive['bid']=self.bestfive['close'].map(bid_dict).fillna(value=0).astype(int)
        self.bestfive['ask']=self.bestfive['close'].map(ask_dict).fillna(value=0).astype(int)
        asklist=self.bestfive['ask'][self.bestfive['ask']!=0].index.tolist()
        bidlist=self.bestfive['bid'][self.bestfive['bid']!=0].index.tolist()
        # # print('bid: ',self.bestfive['bid'].to_dict())
        self.lastbidlist=list(set(self.lastbidlist+bidlist))
        self.lastasklist=list(set(self.lastasklist+asklist))
        self.bestfive.loc[self.lastbidlist,'bidTBitem'].map(lambda x : x.setText(str(self.bestfive.loc[self.bestfive['bidTBitem'][self.bestfive['bidTBitem']==x].index[0],'bid'])) if self.bestfive.loc[self.bestfive['bidTBitem'][self.bestfive['bidTBitem']==x].index[0],'bid']!=0 else x.setText('') )
        self.bestfive.loc[self.lastasklist,'askTBitem'].map(lambda x : x.setText(str(self.bestfive.loc[self.bestfive['askTBitem'][self.bestfive['askTBitem']==x].index[0],'ask'])) if self.bestfive.loc[self.bestfive['askTBitem'][self.bestfive['askTBitem']==x].index[0],'ask']!=0 else x.setText('') )
        # self.lastclose=self.bestfive['close'].tolist()
        self.lastbidlist=bidlist
        self.lastasklist=asklist
    # 閃電下單結束
    # 報價系統連線功能
    def ConnectFun(self):
        m_nCode=skQ.SKQuoteLib_EnterMonitor()
        self.SKMessage.textBrowser.append(str(m_nCode))
    def disconnectFun(self):
        m_nCode=skQ.SKQuoteLib_LeaveMonitor()
        self.SKMessage.textBrowser.append(str(m_nCode))
    # 報價系統結束
    # 商品訂閱
    def commodityFnc(self):
        nstock=self.commodityline.text().replace(' ','')
        self.Future = tickstokline.dataprocess(nstock)
        skQ.SKQuoteLib_RequestTicks(0,nstock)
        # skQ.SKQuoteLib_RequestLiveTick(0,nstock)
        self.ndetialmsg=FuncUI.MessageDialog(nstock)
        self.TDetailbtn.clicked.connect(self.ndetialmsg.show)
        # self.ndetialmsg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.ndetialmsg.show()
        self.DomTableUI()#閃電下單介面
        self.Kitem=KlineUi.CandlestickItem()
        self.Kui=KlineUi.KlineWidget(nstock)
        self.Kui.addItem(self.Kitem)
        self.Kitem.set_data(self.Future.contractkpd)
        self.TableThrd=TableThread()
        self.TableThrd.start()
        xmax=int(len(self.Kitem.pictures))
        xmin=int(max(0,xmax-self.Kitem.countK))
        ymin=self.Kitem.data.loc[xmin:xmax,['low']].values.min()
        ymax=self.Kitem.data.loc[xmin:xmax,['high']].values.max()
        self.GL.addWidget(self.Kui)
        # app.processEvents()   
        self.Kui.update(xmin,xmax,ymin,ymax,self.Kitem.FPS)
    # 商品訂閱結束
# 多執行續 閃電下單
class TableThread(QThread):
    Table_signal=pyqtSignal(int,dict)

    def __init__(self,parent=None):
        super(TableThread,self).__init__(parent)
        self.Table_signal.connect(self.TableFunc)

    def TableFunc(self,nclose,total_dict):
        SKMain.DomTableFillFunc(nclose,total_dict['bid_dict'],total_dict['ask_dict'])

class SKOrderLibEvent:
    def OnAccount(self,bstrLogInID,bstrAccountData):
        Line=bstrAccountData.split(',')
        if Line[0]=='TF':
            bstrAccount=str(Line[1]).strip()+str(Line[3]).strip()
            print('期貨帳戶: '+bstrAccount,',',Line[5])
            m_nCode=skO.GetFutureRights(bstrLogInID,bstrAccount,1)
            m_nCode=skO.ReadCertByID(bstrLogInID)
            m_nCode = skR.SKReplyLib_ConnectByID(bstrLogInID)
            SKMain.SKMessage.textBrowser.append(str(m_nCode))
    
    def OnFutureRights(self,bstrData):
        Line=bstrData.split(',')
        i=0
        for row in Line:
            if row.find('##')>=0:
                break
            else:
                if row.find('+')>=0 :
                    SKMain.Bill.loc[i,'Right'].setText(str(int(row.replace('+','').strip())))
                else :
                    SKMain.Bill.loc[i,'Right'].setText(row.strip())
            i+=1
    def OnOpenInterest(self,bstrData):
        print(bstrData)

class SKReplyLibEvent:
    def OnConnect(self,bstrUserID,nErrorCode):
        nErrorStr=skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        print('連線成功: ',bstrUserID,nErrorStr)
    def OnDisconnect(self,bstrUserID,nErrorCode):
        nErrorStr=skC.SKCenterLib_GetReturnCodeMessage(nErrorCode)
        print('連線失敗: ',bstrUserID,nErrorStr)
    def OnComplete(self,bstrUserID):
        print('回報完成: ',bstrUserID)
    def OnNewData(self,bstrUserID,bstrData):
        Line=bstrData.split(',')
        i=0
        for row in Line :
            print(i,',',row)
            i+=1
    def OnSmartData(self,bstrUserID,bstrData):
        print(bstrData,'智動回報:',bstrData)

class SKQuoteLibEvents:
     
    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!"
        elif (nKind == 3002):
            strMsg = "DisConnected!"
        elif (nKind == 3003):
            strMsg = "Stocks ready!"
        elif (nKind == 3021):
            strMsg = "Connect Error!"
        # print(strMsg)
        SKMain.SKMessage.textBrowser.append(strMsg)

    def OnNotifyServerTime(self,sHour,sMinute,sSecond,nTotal):
        nTime=QTime(sHour,sMinute,sSecond)
        jTime=QTime(13,50,00)
        # jTime=datetime.datetime.strptime('13:50:00','%H:%M:%S').time()
        if nTime==jTime and SKMain.Future.ticksdf is not None :
            filename='data/Ticks'+str(SKMain.Future.ticksdf.iloc[-1,0])+'.txt'
            SKMain.Future.ticksdf.to_csv(filename,header=False,index=False)
        nTime=QTime(sHour,sMinute,sSecond).toString(Qt.ISODate)
        SKMain.statusBar.showMessage('帳號:'+str(SKMain.SKID)+'\t伺服器時間:'+nTime)
    
    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        # strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        if nSimulate==0:
            SKMain.Future.Ticks(lDate,lTimehms,lTimemillismicros,nBid,nAsk,nClose,nQty)
            strMsg=str(SKMain.Future.contractkpd.iloc[-1:].values)
            SKMain.ndetialmsg.textBrowser.append(strMsg)
    
    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        # strMsg=str(lDate)+','+str(lTimehms)+','+str(lTimemillismicros)+','+str(nBid)+','+str(nAsk)+','+str(nClose)+','+str(nQty)
        if nSimulate==0:
            SKMain.Future.Ticks(lDate,lTimehms,lTimemillismicros,nBid,nAsk,nClose,nQty)
            strMsg=str(SKMain.Future.contractkpd.iloc[-1:].values)
            SKMain.ndetialmsg.textBrowser.append(strMsg)
            SKMain.Kitem.set_data(SKMain.Future.contractkpd)
            xmax=int(len(SKMain.Kitem.pictures))
            xmin=int(max(0,xmax-SKMain.Kitem.countK))
            ymin=SKMain.Kitem.data.loc[xmin:xmax,['low']].values.min()
            ymax=SKMain.Kitem.data.loc[xmin:xmax,['high']].values.max()
            SKMain.Kui.update(xmin,xmax,ymin,ymax,SKMain.Kitem.FPS)
    def OnNotifyBest5(self,sMarketNo,sStockidx,nBestBid1,nBestBidQty1,nBestBid2,nBestBidQty2,nBestBid3,nBestBidQty3,nBestBid4,nBestBidQty4,nBestBid5,nBestBidQty5,nExtendBid,nExtendBidQty,nBestAsk1,nBestAskQty1,nBestAsk2,nBestAskQty2,nBestAsk3,nBestAskQty3,nBestAsk4,nBestAskQty4,nBestAsk5,nBestAskQty5,nExtendAsk,nExtendAskQty,nSimulate):
            total_dict={'bid_dict':{int(nBestBid1/100):int(nBestBidQty1),int(nBestBid2/100):int(nBestBidQty2),int(nBestBid3/100):int(nBestBidQty3),int(nBestBid4/100):int(nBestBidQty4),int(nBestBid5/100):int(nBestBidQty5)},
            'ask_dict':{int(nBestAsk1/100):int(nBestAskQty1),int(nBestAsk2/100):int(nBestAskQty2),int(nBestAsk3/100):int(nBestAskQty3),int(nBestAsk4/100):int(nBestAskQty4),int(nBestAsk5/100):int(nBestAskQty5)}}
            SKMain.TableThrd.Table_signal.emit(SKMain.Future.contractkpd.iloc[-1,4],total_dict)
            # 更新點

#comtypes使用此方式註冊callback
SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)
SKOrderEvent = SKOrderLibEvent()
SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)
SKReplyEvent=SKReplyLibEvent()
SKReplyLibEventHandler = comtypes.client.GetEvents(skR, SKReplyEvent)


if __name__ == "__main__":
    SKApp=QApplication(sys.argv)
    SKMain=SKMainWindow()
    SKMain.show()
    sys.exit(SKApp.exec_())