import { UserType } from "@/types/user";
import Image from 'next/image'
import './user.css';

export default function User({id,name,ico}:UserType){
    const src = ico || '/favicon.ico'
    return (
        <span className="user">
            <span className="user-icon">
                <Image src={src} alt={`${name} icon`} width={16} height={16} />
            </span>
            {name}
        </span>
    )
}