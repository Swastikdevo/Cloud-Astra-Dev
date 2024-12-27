```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');

    const addCustomer = () => {
        if(name && email) {
            setCustomers([...customers, { name, email }]);
            setName('');
            setEmail('');
        }
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                value={name} 
                placeholder="Customer Name" 
                onChange={(e) => setName(e.target.value)} 
            />
            <input 
                type="email" 
                value={email} 
                placeholder="Customer Email" 
                onChange={(e) => setEmail(e.target.value)} 
            />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```