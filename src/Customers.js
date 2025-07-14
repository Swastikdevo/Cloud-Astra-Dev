```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');

    const addCustomer = (e) => {
        e.preventDefault();
        if (name && email) {
            setCustomers([...customers, { name, email }]);
            setName('');
            setEmail('');
        }
    };

    const deleteCustomer = (index) => {
        const newCustomers = customers.filter((_, i) => i !== index);
        setCustomers(newCustomers);
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <form onSubmit={addCustomer}>
                <input 
                    type="text" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    placeholder="Customer Name" 
                    required 
                />
                <input 
                    type="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Customer Email" 
                    required 
                />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>
                        {customer.name} - {customer.email} 
                        <button onClick={() => deleteCustomer(index)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```