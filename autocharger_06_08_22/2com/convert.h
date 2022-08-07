
String two_complement(String _data,char _buf[16]){
    int _size = _data.length();
    char result[_size];
    _data.toUpperCase();
    _data.toCharArray(_buf, 50);
    for (int i = 0; i< _data.length();i++){
      switch (_buf[i]) {
      case '0': result[i] = 'F'; break;
      case '1': result[i] = 'E'; break;
      case '2': result[i] = 'D'; break;
      case '3': result[i] = 'C';break;
      case '4': result[i] = 'B';break;
      case '5': result[i] = 'A';break;
      case '6': result[i] = '9';break;
      case '7': result[i] = '8';break;
      case '8': result[i] = '7';break;
      case '9': result[i] = '6';break;
      case 'A': result[i] = '5';break;
      case 'B': result[i] = '4';break;
      case 'C': result[i] = '3';break;
      case 'D': result[i] = '2';break;
      case 'E': result[i] = '1';break;
      case 'F': result[i] = '0';break;
      }
      }
       switch (result[_size - 1]) {
        case '0' :result[_size - 1] = '1'; break;
        case '1' :result[_size - 1] = '2'; break;
        case '2' :result[_size - 1] = '3'; break;
        case '3' :result[_size - 1] = '4'; break;
        case '4' :result[_size - 1] = '5'; break;
        case '5' :result[_size - 1] = '6'; break;        
        case '6' :result[_size - 1] = '7'; break;
        case '7' :result[_size - 1] = '8'; break;
        case '8' :result[_size - 1] = '9'; break;
        case '9' :result[_size - 1] = 'A'; break;
        case 'A' :result[_size - 1] = 'B'; break;
        case 'B' :result[_size - 1] = 'C'; break;
        case 'C' :result[_size - 1] = 'D'; break;
        case 'D' :result[_size - 1] = 'E'; break;
        case 'E' :result[_size - 1] = 'F'; break;
        case 'F' :result[_size - 1] = '0'; break;
       }
       return String(result);
   }
