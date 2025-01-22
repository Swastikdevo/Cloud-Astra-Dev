```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [customerName, setCustomerName] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const addCustomer = () => {
        if (customerName) {
            const newCustomer = { name: customerName };
            setCustomers([...customers, newCustomer]);
            setCustomerName('');
        }
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Search..." 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
            />
            <div>
                <input 
                    type="text" 
                    value={customerName} 
                    onChange={(e) => setCustomerName(e.target.value)} 
                    placeholder="Add Customer" 
                />
                <button onClick={addCustomer}>Add</button>
            </div>
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```