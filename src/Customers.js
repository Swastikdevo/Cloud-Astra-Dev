```javascript
import React, { useState } from 'react';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [editIndex, setEditIndex] = useState(-1);

    const handleAddCustomer = () => {
        if (editIndex >= 0) {
            const updatedCustomers = [...customers];
            updatedCustomers[editIndex] = name;
            setCustomers(updatedCustomers);
            setEditIndex(-1);
        } else {
            setCustomers([...customers, name]);
        }
        setName('');
    };

    const handleEditCustomer = (index) => {
        setName(customers[index]);
        setEditIndex(index);
    };

    const handleDeleteCustomer = (index) => {
        setCustomers(customers.filter((_, i) => i !== index));
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Enter Customer Name" 
            />
            <button onClick={handleAddCustomer}>{editIndex >= 0 ? 'Update' : 'Add'}</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>
                        {customer}
                        <button onClick={() => handleEditCustomer(index)}>Edit</button>
                        <button onClick={() => handleDeleteCustomer(index)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Customers;
```