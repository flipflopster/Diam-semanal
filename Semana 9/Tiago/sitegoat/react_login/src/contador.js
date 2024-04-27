import React, {useState} from 'react';

function Contador() {

 const [count, setCount] = useState(0);

 return (
     <div>
     <h1> Nºvezes: {count}</h1>

      <button onClick={() => setCount(count + 1)}>Incrementa o contador</button>

     </div>
 );
}

export default Contador();