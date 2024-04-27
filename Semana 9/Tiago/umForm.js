import React, {useState} from 'react';

function UmForm() {
 const [nome, setNome] = useState("");
 const handleSubmit = (event) => {
     event.preventDefault();
     alert(`Nome introduzido: ${nome}`);
 }
 return (
     <form onSubmit={handleSubmit}>
         <label>Nome:
             <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} />
        </label>
         <input type="submit" />
    </form>
 )
}
export default UmForm();