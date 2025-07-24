```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    
    useEffect(() => {
        // Fetch initial customer data
        const fetchData = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchData();
    }, []);

    const addCustomer = () => {
        const newCustomer = { name, email };
        setCustomers([...customers, newCustomer]);
        setName('');
        setEmail('');
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management System</h1>
            <input 
                type="text" 
                placeholder="Search customers..." 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
            />
            <div>
                <input 
                    type="text" 
                    placeholder="Name" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                />
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                />
                <button onClick={addCustomer}>Add Customer</button>
            </div>
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManager;
```