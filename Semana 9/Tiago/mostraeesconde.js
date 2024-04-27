import React,{useState} from "react";
function Mostraeesconde(){

    const [isVisible,setIsVisible] = useState(true);
    return <div>
        {isVisible &&
            <p>Texto para mostrar</p>
        }
        <button onClick={() => setIsVisible(!isVisible)}>Ocultar Texto</button>
    </div>
}
// if isVisicle then -> {isVisible &&
export default Mostraeesconde();