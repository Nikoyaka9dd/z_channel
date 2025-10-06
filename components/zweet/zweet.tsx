import "./zweet.css";
import type { ZweetProps, UserProps } from '../../types/zweet';

export default function Zweet({
    id,content,user,createdAt,good,reply,retweet
}:ZweetProps){
    return (
    <div className="zweet-main">
        <div >
            <User 
                user={user}
            />
            <div>{content}</div>

        </div>
        <div>
            <span>👍 {good}</span>
            <span>reply {reply}</span>
            <span>retweet {retweet}</span>
        </div>
        <div>{createdAt}</div>
    </div>
    )
}

export function User({user}: UserProps){
    return (
        <div className="user">
            {user.username}
        </div>
    )
}