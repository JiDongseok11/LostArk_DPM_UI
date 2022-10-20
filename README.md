pyqt5 폴더 안에 sample.qt 실행시키면 프로그램 실행됨

지금 입력은 클래스, 유물, 수치 값 4개, 각인 입력 받을 수 있게 해놨고
시뮬레이션 돌리는거는 수치 값 제외하고 클래스, 유물, 각인만 넣고 돌아가게 해놓음

사실 저 수치 값은 뭐 입력해야 되는건지 모르겠는데
그 character_settings 안에 upgrade, crit, specialization, swiftness 이거 4개 있길래 일단 입력 받아서 
character setting 형태 json으로 저장까지 할 수 있는 상태임

해야되는거:
1. 각인 중복 선택 안되게 하기
2. cirt, specialization, swiftness tag 추가
3. cirt, specialization, swiftness simulator에 반영
4. result window에 결과 display
