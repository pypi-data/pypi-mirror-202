def minMaxAvg(testlist):
    """
    최소 최댓값을 뺀 평균
    parameter : testlist = 리스트 
    return : 리스트내 값에서 최소 최대값을 뺀 평균을 반환한다
    """
    minValue = min(testlist)
    maxValue = max(testlist)

    print('최소값 : {} ,최대값 :  {}'.format(minValue,maxValue))

    testlist.remove(minValue)
    testlist.remove(maxValue)

    if len(testlist) !=0 :
        average  = sum(testlist) / len(testlist)
    else: 
        pass
    
    return average

def round_desc(in_value,point=2):        
    """
    소수 셋째자리까지 구하는 함수 
    parameter : in_value = float 타입 ,point = int 타입 ->default는 2로 인자를 넣지않으면 2를 사용
    return : 값에 100을 곱하고 int로 캐스팅한뒤 round_point으로 나누어 더블형으로 반환
    """
    round_point = 10 ** point
    change_num = in_value * round_point
    change_num = int(change_num)     
    change_num = change_num / round_point
    return change_num                        #구한 값 return


#일
def theDayBefore(inputDate, days):
    """
    입력한 날짜로부터 일수만큼 이전 날짜를 반환하는 함수
    parameter : inputDate-YYYYMMDD(int) days-일수(int)
    return : input 날짜로부터 일수(days)만큼 이전 날짜
    """

    inputDate = str(inputDate)
    #inputDate = "20230508"
    #days = 158000
    inputYear = inputDate[:4]
    inputMonth = inputDate[4:6]
    inputDay = inputDate[6:]

    # 1~9일의 정확한 비교를 위해 0을 제거
    if inputMonth < '10':
         inputMonth = inputMonth[1:]

    if inputDay < '10':
         inputDay = inputDay[1:]

    for i in range(days):

        # 이전 날짜 계산
        if inputDay == '1':  # 달이 바뀌는 경우
            if inputMonth == '1':  # 달과 연도가 모두 바뀌는 경우 (1월 1일) -> 연도도 마이너스, 월도 12월로 세팅
                inputYear = str(int(inputYear) - 1)
                inputMonth = '12'
                monthDays = 31
            else: # 달이 변경, 연도는 그대로 (1월을 제외한 n월 1일) -> 월을 마이너스하고, 해당 월에 맞춰 일자 세팅
                inputMonth = str(int(inputMonth) - 1)
                if (inputMonth=='4'or inputMonth=='6'or inputMonth=='9'or inputMonth=='11'):
                    monthDays = 30
                elif inputMonth=='2' :
                    if int(inputYear) % 4 == 0 and int(inputYear) % 100 != 0 or int(inputYear) % 400 == 0:
                        monthDays = 29  # 윤년인 경우 29일
                    else:
                        monthDays = 28  # 평년인 경우 28일 
                else :
                    monthDays = 31
            inputDay = str(monthDays)
        else:  # 달이 바뀌지 않는 경우 -> 일자만 마이너스
            inputDay = str(int(inputDay) - 1)

    # 반복 끝나고 나면, inputMonth와 inputDay에 다시 0을 붙여주기
    if int(inputMonth) < 10 :
        inputMonth = '0' + str(inputMonth)

    if int(inputDay) < 10 :
        inputDay = '0' + str(inputDay)

        #return int(inputYear + inputMonth + inputDay)
    return int(inputYear + inputMonth + inputDay)


#주
from isoweek import Week

def calyearWeek(yearWeek,y):
    """
    주차 계산
    parameter(입력값) x: 기준 년도와 주차 y : 빼고싶은 주차
    return : 기준 년도에서 빼고싶은 주차를 뺀 값 : x와 형식 동일
    """

       

    # 년도와 주차를 인덱스로 나누기 위해 String으로
    inputdata = str(yearWeek)

    inputyear = inputdata[:4]

    inputweek = inputdata[4:]

    # 계산하기 위해 다시 숫자로
    proceccedYear = int(inputyear)
    proceccedYear


    proceccedWeek = int(inputweek)
    proceccedWeek


    fuc = Week.last_week_of_year(proceccedYear).week
    fuc

    # 년도가 넘어가는지 안넘어가는지 판단. 안넘어가는 상황은 break 
    for i in range(0,9999) :

        if proceccedWeek > y :  
            proceccedWeek=proceccedWeek-y
            resulT = [proceccedYear,proceccedWeek]
            break


        elif proceccedWeek <= y : 

            proceccedYear=proceccedYear-1
            y = abs(proceccedWeek-y)
            fuc = Week.last_week_of_year(proceccedYear).week
            proceccedWeek = fuc



    return resulT[0]*100+resulT[1]

#달
import datetime
from dateutil.relativedelta import relativedelta
def monthCal(yearMonthDay, dayCal):
    
    '''
    과거와 미래 둘다 한번에 예측
    parameter : string or int 타입으로 데이터를 입력받으며 
                daycal의 경우 +,-로 과거와 미래로 예측을 해줍니다.
    return    : datetime.date 타입으로 출력해줍니다.
    '''
    year = 0
    month = 0
    day = 0
    dividyear = 4
    dividmonth = 6
    
    # 년도,월,일로 나누는 처리 과정

    if type(yearMonthDay) == str :
            year  = yearMonthDay[:dividyear]
            month = yearMonthDay[dividyear:dividmonth]
            day = yearMonthDay[dividmonth:]
            year = int(year)
            month = int(month)
            day = int(day)


    if type(dayCal) == str:
            dayCal = int(dayCal)

    # 연도,월,일 그리고 이동하는 숫자의 경우 string의 타입이면
    # 연산을 쉅게 수행하기위해서 int 형으로 형 변환을 해줍니다.        
            
    checkMonth = datetime.date(year,month,day) + relativedelta(months=dayCal)
    
    # relativedelta 함수를 이용한다면 차이나는 날짜를 넣음으로써 datetime의 객체를 만들어준다.
    
    return checkMonth

    # return 값은 datetime.date 형태로 반환합니다.