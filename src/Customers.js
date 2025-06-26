```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        fetch('https://api.example.com/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search customers" 
                value={searchTerm} 
                onChange={e => setSearchTerm(e.target.value)} 
            />
            {loading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {filteredCustomers.map(customer => (
                        <li key={customer.id}>{customer.name}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerList;
```